//This file is automatically rebuilt by the Cesium build process.
export default "vec3 czm_acesTonemapping(vec3 color) {\n\
float g = 0.985;\n\
float a = 0.065;\n\
float b = 0.0001;\n\
float c = 0.433;\n\
float d = 0.238;\n\
color = (color * (color + a) - b) / (color * (g * color + c) + d);\n\
color = clamp(color, 0.0, 1.0);\n\
return color;\n\
}\n\
";
