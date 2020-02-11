/* This file is automatically rebuilt by the Cesium build process. */
define(['./when-76089d4c', './Check-5cd4f88e', './Math-4da9b357', './Cartesian2-88a9081c', './defineProperties-7057a760', './Transforms-30697ad4', './RuntimeError-bd79d86c', './WebGLConstants-e4e9c6cc', './ComponentDatatype-7dd74ff6', './GeometryAttribute-46ce3b25', './GeometryAttributes-36724c9f', './IndexDatatype-7c4ae249', './GeometryOffsetAttribute-b8954087', './VertexFormat-c83968d5', './EllipsoidGeometry-f64a47e9'], function (when, Check, _Math, Cartesian2, defineProperties, Transforms, RuntimeError, WebGLConstants, ComponentDatatype, GeometryAttribute, GeometryAttributes, IndexDatatype, GeometryOffsetAttribute, VertexFormat, EllipsoidGeometry) { 'use strict';

    function createEllipsoidGeometry(ellipsoidGeometry, offset) {
            if (when.defined(offset)) {
                ellipsoidGeometry = EllipsoidGeometry.EllipsoidGeometry.unpack(ellipsoidGeometry, offset);
            }
            return EllipsoidGeometry.EllipsoidGeometry.createGeometry(ellipsoidGeometry);
        }

    return createEllipsoidGeometry;

});
