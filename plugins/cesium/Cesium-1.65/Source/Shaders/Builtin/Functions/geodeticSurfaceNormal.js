//This file is automatically rebuilt by the Cesium build process.
export default "vec3 czm_geodeticSurfaceNormal(vec3 positionOnEllipsoid, vec3 ellipsoidCenter, vec3 oneOverEllipsoidRadiiSquared)\n\
{\n\
return normalize((positionOnEllipsoid - ellipsoidCenter) * oneOverEllipsoidRadiiSquared);\n\
}\n\
";
