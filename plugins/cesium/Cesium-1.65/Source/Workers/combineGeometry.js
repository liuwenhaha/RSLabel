/* This file is automatically rebuilt by the Cesium build process. */
define(['./when-76089d4c', './Check-5cd4f88e', './Math-4da9b357', './Cartesian2-88a9081c', './defineProperties-7057a760', './Transforms-30697ad4', './RuntimeError-bd79d86c', './WebGLConstants-e4e9c6cc', './ComponentDatatype-7dd74ff6', './GeometryAttribute-46ce3b25', './GeometryAttributes-36724c9f', './AttributeCompression-3a5fff57', './GeometryPipeline-813331d2', './EncodedCartesian3-e0dcfcb4', './IndexDatatype-7c4ae249', './IntersectionTests-654d9c0a', './Plane-b1ef5cca', './PrimitivePipeline-8d61357f', './WebMercatorProjection-b2b73805', './createTaskProcessorWorker'], function (when, Check, _Math, Cartesian2, defineProperties, Transforms, RuntimeError, WebGLConstants, ComponentDatatype, GeometryAttribute, GeometryAttributes, AttributeCompression, GeometryPipeline, EncodedCartesian3, IndexDatatype, IntersectionTests, Plane, PrimitivePipeline, WebMercatorProjection, createTaskProcessorWorker) { 'use strict';

    function combineGeometry(packedParameters, transferableObjects) {
            var parameters = PrimitivePipeline.PrimitivePipeline.unpackCombineGeometryParameters(packedParameters);
            var results = PrimitivePipeline.PrimitivePipeline.combineGeometry(parameters);
            return PrimitivePipeline.PrimitivePipeline.packCombineGeometryResults(results, transferableObjects);
        }
    var combineGeometry$1 = createTaskProcessorWorker(combineGeometry);

    return combineGeometry$1;

});
