FilePond.registerPlugin(
    FilePondPluginImageResize,
    FilePondPluginImageTransform
  );

const inputElement = document.querySelector('input[type="file"]');
const pond = FilePond.create(inputElement, {
    imageResizeTargetWidth: 1024,
    
    // set contain resize mode
    imageResizeMode: 'contain',
    
    onaddfile: (err, fileItem) => {
        console.log(err, fileItem.getMetadata('resize'));
    },
    
    onpreparefile: (fileItem, output) => {
        const img = new Image();
        img.src = URL.createObjectURL(output);
        document.body.appendChild(img);
    }
});
  