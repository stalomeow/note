# Lighting, Materials and Shaders

## ~~图形学黑话~~

1. **Radiance:** 射出去的光
2. **Irradiance:** Incoming Radiance 的缩写。射进来的光。

## 渲染方程
Kajiya 大佬在 1986 年 SIGGRAPH 里提出 "The rendering equation":

$$
L_o(\mathbf{x}, \omega_o) = L_e(\mathbf{x}, \omega_o) + \int_{H^2}f_r(\mathbf{x}, \omega_o, \omega_i)L_i(\mathbf{x}, \omega_i)\cos\theta_i\,d\omega_i
$$

意思就是 射出去的光 = 自发光 + 反射的光。