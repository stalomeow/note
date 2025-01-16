'use strict';

var obsidian = require('obsidian');

/******************************************************************************
Copyright (c) Microsoft Corporation.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
***************************************************************************** */

function __awaiter(thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
}

const DEFAULT_SETTINGS = {
    enableAutoSuggest: true,
    enableFootnoteSectionHeading: false,
    FootnoteSectionHeading: "Footnotes",
};
class FootnotePluginSettingTab extends obsidian.PluginSettingTab {
    constructor(app, plugin) {
        super(app, plugin);
        this.plugin = plugin;
    }
    display() {
        const { containerEl } = this;
        containerEl.empty();
        containerEl.createEl("h2", {
            text: "Footnote Shortcut",
        });
        const mainDesc = containerEl.createEl('p');
        mainDesc.appendText('Need help? Check the ');
        mainDesc.appendChild(createEl('a', {
            text: "README",
            href: "https://github.com/MichaBrugger/obsidian-footnotes",
        }));
        mainDesc.appendText('!');
        containerEl.createEl('br');
        new obsidian.Setting(containerEl)
            .setName("Enable Footnote Autosuggest")
            .setDesc("Suggests existing footnotes when entering named footnotes.")
            .addToggle((toggle) => toggle
            .setValue(this.plugin.settings.enableAutoSuggest)
            .onChange((value) => __awaiter(this, void 0, void 0, function* () {
            this.plugin.settings.enableAutoSuggest = value;
            yield this.plugin.saveSettings();
        })));
        containerEl.createEl("h3", {
            text: "Footnotes Section Behavior",
        });
        new obsidian.Setting(containerEl)
            .setName("Enable Footnote Section Heading")
            .setDesc("Automatically adds a heading separating footnotes at the bottom of the note from the rest of the text.")
            .addToggle((toggle) => toggle
            .setValue(this.plugin.settings.enableFootnoteSectionHeading)
            .onChange((value) => __awaiter(this, void 0, void 0, function* () {
            this.plugin.settings.enableFootnoteSectionHeading = value;
            yield this.plugin.saveSettings();
        })));
        new obsidian.Setting(containerEl)
            .setName("Footnote Section Heading")
            .setDesc("Heading to place above footnotes section (Supports Markdown formatting). Heading will be H1 size.")
            .addText((text) => text
            .setPlaceholder("Heading is Empty")
            .setValue(this.plugin.settings.FootnoteSectionHeading)
            .onChange((value) => __awaiter(this, void 0, void 0, function* () {
            this.plugin.settings.FootnoteSectionHeading = value;
            yield this.plugin.saveSettings();
        })));
    }
}

var AllMarkers = /\[\^([^\[\]]+)\](?!:)/dg;
var AllNumberedMarkers = /\[\^(\d+)\]/gi;
var AllDetailsNameOnly = /\[\^([^\[\]]+)\]:/g;
var DetailInLine = /\[\^([^\[\]]+)\]:/;
var ExtractNameFromFootnote = /(\[\^)([^\[\]]+)(?=\])/;
function listExistingFootnoteDetails(doc) {
    let FootnoteDetailList = [];
    //search each line for footnote details and add to list
    for (let i = 0; i < doc.lineCount(); i++) {
        let theLine = doc.getLine(i);
        let lineMatch = theLine.match(AllDetailsNameOnly);
        if (lineMatch) {
            let temp = lineMatch[0];
            temp = temp.replace("[^", "");
            temp = temp.replace("]:", "");
            FootnoteDetailList.push(temp);
        }
    }
    if (FootnoteDetailList.length > 0) {
        return FootnoteDetailList;
    }
    else {
        return null;
    }
}
function listExistingFootnoteMarkersAndLocations(doc) {
    let markerEntry;
    let FootnoteMarkerInfo = [];
    //search each line for footnote markers
    //for each, add their name, line number, and start index to FootnoteMarkerInfo
    for (let i = 0; i < doc.lineCount(); i++) {
        let theLine = doc.getLine(i);
        let lineMatch;
        while ((lineMatch = AllMarkers.exec(theLine)) != null) {
            markerEntry = {
                footnote: lineMatch[0],
                lineNum: i,
                startIndex: lineMatch.index
            };
            FootnoteMarkerInfo.push(markerEntry);
        }
    }
    return FootnoteMarkerInfo;
}
function shouldJumpFromDetailToMarker(lineText, cursorPosition, doc) {
    // check if we're in a footnote detail line ("[^1]: footnote")
    // if so, jump cursor back to the footnote in the text
    let match = lineText.match(DetailInLine);
    if (match) {
        let s = match[0];
        let index = s.replace("[^", "");
        index = index.replace("]:", "");
        let footnote = s.replace(":", "");
        let returnLineIndex = cursorPosition.line;
        // find the FIRST OCCURENCE where this footnote exists in the text
        for (let i = 0; i < doc.lineCount(); i++) {
            let scanLine = doc.getLine(i);
            if (scanLine.contains(footnote)) {
                let cursorLocationIndex = scanLine.indexOf(footnote);
                returnLineIndex = i;
                doc.setCursor({
                    line: returnLineIndex,
                    ch: cursorLocationIndex + footnote.length,
                });
                return true;
            }
        }
    }
    return false;
}
function shouldJumpFromMarkerToDetail(lineText, cursorPosition, doc) {
    // Jump cursor TO detail marker
    // does this line have a footnote marker?
    // does the cursor overlap with one of them?
    // if so, which one?
    // find this footnote marker's detail line
    // place cursor there
    let markerTarget = null;
    let FootnoteMarkerInfo = listExistingFootnoteMarkersAndLocations(doc);
    let currentLine = cursorPosition.line;
    let footnotesOnLine = FootnoteMarkerInfo.filter((markerEntry) => markerEntry.lineNum === currentLine);
    if (footnotesOnLine != null) {
        for (let i = 0; i <= footnotesOnLine.length - 1; i++) {
            if (footnotesOnLine[i].footnote !== null) {
                let marker = footnotesOnLine[i].footnote;
                let indexOfMarkerInLine = footnotesOnLine[i].startIndex;
                if (cursorPosition.ch >= indexOfMarkerInLine &&
                    cursorPosition.ch <= indexOfMarkerInLine + marker.length) {
                    markerTarget = marker;
                    break;
                }
            }
        }
    }
    if (markerTarget !== null) {
        // extract name
        let match = markerTarget.match(ExtractNameFromFootnote);
        if (match) {
            let footnoteName = match[2];
            // find the first line with this detail marker name in it.
            for (let i = 0; i < doc.lineCount(); i++) {
                let theLine = doc.getLine(i);
                let lineMatch = theLine.match(DetailInLine);
                if (lineMatch) {
                    // compare to the index
                    let nameMatch = lineMatch[1];
                    if (nameMatch == footnoteName) {
                        doc.setCursor({ line: i, ch: lineMatch[0].length + 1 });
                        return true;
                    }
                }
            }
        }
    }
    return false;
}
function addFootnoteSectionHeader(plugin) {
    //check if 'Enable Footnote Section Heading' is true
    //if so, return the "Footnote Section Heading"
    // else, return ""
    if (plugin.settings.enableFootnoteSectionHeading == true) {
        let returnHeading = `\n# ${plugin.settings.FootnoteSectionHeading}`;
        return returnHeading;
    }
    return "";
}
//FUNCTIONS FOR AUTONUMBERED FOOTNOTES
function insertAutonumFootnote(plugin) {
    const mdView = app.workspace.getActiveViewOfType(obsidian.MarkdownView);
    if (!mdView)
        return false;
    if (mdView.editor == undefined)
        return false;
    const doc = mdView.editor;
    const cursorPosition = doc.getCursor();
    const lineText = doc.getLine(cursorPosition.line);
    const markdownText = mdView.data;
    if (shouldJumpFromDetailToMarker(lineText, cursorPosition, doc))
        return;
    if (shouldJumpFromMarkerToDetail(lineText, cursorPosition, doc))
        return;
    return shouldCreateAutonumFootnote(lineText, cursorPosition, plugin, doc, markdownText);
}
function shouldCreateAutonumFootnote(lineText, cursorPosition, plugin, doc, markdownText) {
    // create new footnote with the next numerical index
    let matches = markdownText.match(AllNumberedMarkers);
    let currentMax = 1;
    if (matches != null) {
        for (let i = 0; i <= matches.length - 1; i++) {
            let match = matches[i];
            match = match.replace("[^", "");
            match = match.replace("]", "");
            let matchNumber = Number(match);
            if (matchNumber + 1 > currentMax) {
                currentMax = matchNumber + 1;
            }
        }
    }
    let footNoteId = currentMax;
    let footnoteMarker = `[^${footNoteId}]`;
    let linePart1 = lineText.substr(0, cursorPosition.ch);
    let linePart2 = lineText.substr(cursorPosition.ch);
    let newLine = linePart1 + footnoteMarker + linePart2;
    doc.replaceRange(newLine, { line: cursorPosition.line, ch: 0 }, { line: cursorPosition.line, ch: lineText.length });
    let lastLineIndex = doc.lastLine();
    let lastLine = doc.getLine(lastLineIndex);
    while (lastLineIndex > 0) {
        lastLine = doc.getLine(lastLineIndex);
        if (lastLine.length > 0) {
            doc.replaceRange("", { line: lastLineIndex, ch: 0 }, { line: doc.lastLine(), ch: 0 });
            break;
        }
        lastLineIndex--;
    }
    let footnoteDetail = `\n[^${footNoteId}]: `;
    let list = listExistingFootnoteDetails(doc);
    if (list === null && currentMax == 1) {
        footnoteDetail = "\n" + footnoteDetail;
        let Heading = addFootnoteSectionHeader(plugin);
        doc.setLine(doc.lastLine(), lastLine + Heading + footnoteDetail);
        doc.setCursor(doc.lastLine() - 1, footnoteDetail.length - 1);
    }
    else {
        doc.setLine(doc.lastLine(), lastLine + footnoteDetail);
        doc.setCursor(doc.lastLine(), footnoteDetail.length - 1);
    }
}
//FUNCTIONS FOR NAMED FOOTNOTES
function insertNamedFootnote(plugin) {
    const mdView = app.workspace.getActiveViewOfType(obsidian.MarkdownView);
    if (!mdView)
        return false;
    if (mdView.editor == undefined)
        return false;
    const doc = mdView.editor;
    const cursorPosition = doc.getCursor();
    const lineText = doc.getLine(cursorPosition.line);
    mdView.data;
    if (shouldJumpFromDetailToMarker(lineText, cursorPosition, doc))
        return;
    if (shouldJumpFromMarkerToDetail(lineText, cursorPosition, doc))
        return;
    if (shouldCreateMatchingFootnoteDetail(lineText, cursorPosition, plugin, doc))
        return;
    return shouldCreateFootnoteMarker(lineText, cursorPosition, doc);
}
function shouldCreateMatchingFootnoteDetail(lineText, cursorPosition, plugin, doc) {
    // Create matching footnote detail for footnote marker
    // does this line have a footnote marker?
    // does the cursor overlap with one of them?
    // if so, which one?
    // does this footnote marker have a detail line?
    // if not, create it and place cursor there
    let reOnlyMarkersMatches = lineText.match(AllMarkers);
    let markerTarget = null;
    if (reOnlyMarkersMatches) {
        for (let i = 0; i <= reOnlyMarkersMatches.length; i++) {
            let marker = reOnlyMarkersMatches[i];
            if (marker != undefined) {
                let indexOfMarkerInLine = lineText.indexOf(marker);
                if (cursorPosition.ch >= indexOfMarkerInLine &&
                    cursorPosition.ch <= indexOfMarkerInLine + marker.length) {
                    markerTarget = marker;
                    break;
                }
            }
        }
    }
    if (markerTarget != null) {
        //extract footnote
        let match = markerTarget.match(ExtractNameFromFootnote);
        //find if this footnote exists by listing existing footnote details
        if (match) {
            let footnoteId = match[2];
            let list = listExistingFootnoteDetails(doc);
            // Check if the list is empty OR if the list doesn't include current footnote
            // if so, add detail for the current footnote
            if (list === null || !list.includes(footnoteId)) {
                let lastLineIndex = doc.lastLine();
                let lastLine = doc.getLine(lastLineIndex);
                while (lastLineIndex > 0) {
                    lastLine = doc.getLine(lastLineIndex);
                    if (lastLine.length > 0) {
                        doc.replaceRange("", { line: lastLineIndex, ch: 0 }, { line: doc.lastLine(), ch: 0 });
                        break;
                    }
                    lastLineIndex--;
                }
                let footnoteDetail = `\n[^${footnoteId}]: `;
                if (list === null || list.length < 1) {
                    footnoteDetail = "\n" + footnoteDetail;
                    let Heading = addFootnoteSectionHeader(plugin);
                    doc.setLine(doc.lastLine(), lastLine + Heading + footnoteDetail);
                    doc.setCursor(doc.lastLine() - 1, footnoteDetail.length - 1);
                }
                else {
                    doc.setLine(doc.lastLine(), lastLine + footnoteDetail);
                    doc.setCursor(doc.lastLine(), footnoteDetail.length - 1);
                }
                return true;
            }
            return;
        }
    }
}
function shouldCreateFootnoteMarker(lineText, cursorPosition, doc, markdownText) {
    //create empty footnote marker for name input
    let emptyMarker = `[^]`;
    doc.replaceRange(emptyMarker, doc.getCursor());
    //move cursor in between [^ and ]
    doc.setCursor(cursorPosition.line, cursorPosition.ch + 2);
    //open footnotePicker popup
}

class Autocomplete extends obsidian.EditorSuggest {
    constructor(plugin) {
        super(plugin.app);
        this.Footnote_Detail_Names_And_Text = /\[\^([^\[\]]+)\]:(.+(?:\n(?:(?!\[\^[^\[\]]+\]:).)+)*)/g;
        this.getSuggestions = (context) => {
            const { query } = context;
            const mdView = app.workspace.getActiveViewOfType(obsidian.MarkdownView);
            const doc = mdView.editor;
            const matches = this.Extract_Footnote_Detail_Names_And_Text(doc);
            const filteredResults = matches.filter((entry) => entry[1].includes(query));
            return filteredResults;
        };
        this.plugin = plugin;
    }
    onTrigger(cursorPosition, doc, file) {
        if (this.plugin.settings.enableAutoSuggest) {
            const mdView = app.workspace.getActiveViewOfType(obsidian.MarkdownView);
            const lineText = doc.getLine(cursorPosition.line);
            mdView.data;
            let reOnlyMarkersMatches = lineText.match(AllMarkers);
            let markerTarget = null;
            let indexOfMarkerInLine = null;
            if (reOnlyMarkersMatches) {
                for (let i = 0; i <= reOnlyMarkersMatches.length; i++) {
                    let marker = reOnlyMarkersMatches[i];
                    if (marker != undefined) {
                        indexOfMarkerInLine = lineText.indexOf(marker);
                        if (cursorPosition.ch >= indexOfMarkerInLine &&
                            cursorPosition.ch <= indexOfMarkerInLine + marker.length) {
                            markerTarget = marker;
                            break;
                        }
                    }
                }
            }
            if (markerTarget != null) {
                //extract footnote
                let match = markerTarget.match(ExtractNameFromFootnote);
                //find if this footnote exists by listing existing footnote details
                if (match) {
                    let footnoteId = match[2];
                    if (footnoteId !== undefined) {
                        this.latestTriggerInfo = {
                            end: cursorPosition,
                            start: {
                                ch: indexOfMarkerInLine + 2,
                                line: cursorPosition.line
                            },
                            query: footnoteId
                        };
                        return this.latestTriggerInfo;
                    }
                }
            }
            return null;
        }
    }
    Extract_Footnote_Detail_Names_And_Text(doc) {
        //search each line for footnote details and add to list
        //save the footnote detail name as capture group 1
        //save the footnote detail text as capture group 2
        let docText = doc.getValue();
        const matches = Array.from(docText.matchAll(this.Footnote_Detail_Names_And_Text));
        return matches;
    }
    renderSuggestion(value, el) {
        el.createEl("b", { text: value[1] });
        el.createEl("br");
        el.createEl("p", { text: value[2] });
    }
    selectSuggestion(value, evt) {
        const { context, plugin } = this;
        if (!context)
            return;
        const mdView = app.workspace.getActiveViewOfType(obsidian.MarkdownView);
        mdView.editor;
        const field = value[1];
        const replacement = `${field}`;
        context.editor.replaceRange(replacement, this.latestTriggerInfo.start, this.latestTriggerInfo.end);
    }
}

//Add chevron-up-square icon from lucide for mobile toolbar (temporary until Obsidian updates to Lucide v0.130.0)
obsidian.addIcon("chevron-up-square", `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-up-square"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"></rect><polyline points="8,14 12,10 16,14"></polyline></svg>`);
class FootnotePlugin extends obsidian.Plugin {
    onload() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.loadSettings();
            this.registerEditorSuggest(new Autocomplete(this));
            this.addCommand({
                id: "insert-autonumbered-footnote",
                name: "Insert / Navigate Auto-Numbered Footnote",
                icon: "plus-square",
                checkCallback: (checking) => {
                    if (checking)
                        return !!this.app.workspace.getActiveViewOfType(obsidian.MarkdownView);
                    insertAutonumFootnote(this);
                },
            });
            this.addCommand({
                id: "insert-named-footnote",
                name: "Insert / Navigate Named Footnote",
                icon: "chevron-up-square",
                checkCallback: (checking) => {
                    if (checking)
                        return !!this.app.workspace.getActiveViewOfType(obsidian.MarkdownView);
                    insertNamedFootnote(this);
                }
            });
            this.addSettingTab(new FootnotePluginSettingTab(this.app, this));
        });
    }
    loadSettings() {
        return __awaiter(this, void 0, void 0, function* () {
            this.settings = Object.assign({}, DEFAULT_SETTINGS, yield this.loadData());
        });
    }
    saveSettings() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.saveData(this.settings);
        });
    }
}

module.exports = FootnotePlugin;


/* nosourcemap */