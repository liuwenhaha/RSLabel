//This file is automatically rebuilt by the Cesium build process.
export default "uniform sampler2D u_depthTexture;\n\
varying vec2 v_textureCoordinates;\n\
void main()\n\
{\n\
gl_FragColor = czm_packDepth(texture2D(u_depthTexture, v_textureCoordinates).r);\n\
}\n\
";
