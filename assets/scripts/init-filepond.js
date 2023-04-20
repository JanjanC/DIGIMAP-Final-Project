FilePond.registerPlugin(FilePondPluginFileValidateType, FilePondPluginImagePreview, FilePondPluginFileValidateSize);

const inputElement = document.querySelector('input[type="file"]');
const pond = FilePond.create(inputElement, {
	storeAsFile: true,
	acceptedFileTypes: ["image/jpg", "image/jpeg", "image/png"],
	maxFileSize: '5mb',
});
