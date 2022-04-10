## About

This is a minimal JavaScript reader for the TRX tractography format. The specifications for this format is [provided here](https://github.com/frheault/tractography_file_format/blob/master/trx_file_memmap/specifications.md). Previously, most tractography tools used their own proprietary [format](https://www.nitrc.org/plugins/mwiki/index.php/surfice:MainPage#Supported_Formats) such as BFLOAT, niml.tract, PDB, [TCK](https://mrtrix.readthedocs.io/en/latest/getting_started/image_data.html#tracks-file-format-tck), [TRK](http://trackvis.org/docs/?subsect=fileformat) and VTK. The TRX format was developed from community [discussions](https://github.com/nipy/nibabel/issues/942) to address the [limitations of the existing formats](https://docs.google.com/document/d/1GOOlG42rB7dlJizu2RfaF5XNj_pIaVl_6rtBSUhsgbE/edit#heading=h.c6igqydj1hrf) and the needs of the users. 

Here a JavaScript implementation of the format is provided

## Live Demo

[NiiVue provides a WebGL live demo of this code](https://niivue.github.io/niivue/features/tracts.html). This can be tested on any device (computer, laptop, phone). A sample TRX file is loaded by default, but users can drag and drop new streamlines in the TRX, TRK and TCK formats.

## Node.JS Command Line Demo

The example code allows the user to specify a trx file and will display properties of the file.

```
$ npm install jszip
$ node trx.mjs dpv.trx
Vertices:32
 First vertex (x,y,z):191.5,-0.5,-0.5
Streamlines: 2
 Vertices in first streamline: 2
dpg (data_per_group) items: 0
dps (data_per_streamline) items: 0
dpv (data_per_vertex) items: 3
  'effect   ' items: 32
  'pval_corr' items: 32
  'pval     ' items: 32
Header (header.json):
{
  DIMENSIONS: [ 192, 192, 55 ],
  VOXEL_TO_RASMM: [ [ 1, 0, 0, 0 ], [ 0, 1, 0, 0 ], [ 0, 0, 1, 0 ], [ 0, 0, 0, 1 ] ],
  NB_VERTICES: 32,
  NB_STREAMLINES: 2
}
Done
```

## Implementation Details

There are several important considerations regarding supporting the TRX format with JavaScript. The provided minimal reader makes some tradeoffs that may not be appropriate for all use cases.

 - The TRX [specification](https://github.com/frheault/tractography_file_format/blob/master/trx_file_memmap/specifications.md) allows uint64 and int64 arrays and demands that offsets are always uint64. However, JavaScript does not natively support these datatypes. This code converts these values to UNSIGNED uint32 and generates an alert if any value is outside this range. Alternative implementations could support these as float64 (with a [flintmax](https://www.mathworks.com/help/matlab/ref/flintmax.html) of 2^53) or as the new [BigInt](https://www.smashingmagazine.com/2019/07/essential-guide-javascript-newest-data-type-bigint/) type.
 - The TRX format allows arrays to use the float16 datatype, which is not native to JavaScript. This code converts these to float32.
 - Be aware that the specification stores NB_STREAMLINES values in the offsets array, with each value pointing to the start of that streamline One must use the length of the positions array or the header to infer the end of the final streamline. This code will populate return an offset array with NB_STREAMLINES+1 values to solve the [fencepost problem](https://icarus.cs.weber.edu/~dab/cs1410/textbook/3.Control/fencepost.html) for the final streamline. This simplifies and accelerates display code, but one must be aware of this modification.

