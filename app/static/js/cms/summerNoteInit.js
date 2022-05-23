export const initializeSummerNote = (id, placeholder, tabsize=2, height=400) => {
    $(`#${id}`).summernote({
        placeholder: placeholder,
        tabsize: tabsize,
        height: height,
        toolbar: [
          ['style', ['style']],
          ['font', ['bold', 'underline', 'clear']],
          ['color', ['color']],
          ['para', ['ul', 'ol', 'paragraph']],
          ['table', ['table']],
          ['insert', ['link', 'picture', 'video']],
          ['view', ['fullscreen', 'codeview', 'help']]
        ]
      });
};