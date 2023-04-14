FilePond.registerPlugin(FilePondPluginFileValidateType, FilePondPluginImagePreview);

const inputElement = document.querySelector('input[type="file"]');
const pond = FilePond.create(inputElement, {
	storeAsFile: true,
	// labelIdle: "<p>Upload Image</p><p>*png, *jpg, or *jpeg</p>",
	acceptedFileTypes: ["image/jpg", "image/jpeg", "image/png"],
});
