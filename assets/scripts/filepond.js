FilePond.registerPlugin(
    FilePondPluginImagePreview,
    FilePondPluginImageResize,
    FilePondPluginImageTransform
  );

const inputElement = document.querySelector('input[type="file"]');
const pond = FilePond.create(inputElement, {
    storeAsFile: true,
    imageResizeTargetWidth: 1024,
    imageResizeMode: 'cover',
    
    onaddfile: (err, fileItem) => {
        console.log(err, fileItem.getMetadata('resize'));
    }
});
  