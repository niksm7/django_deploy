var script = document.createElement('script');
script.type = 'text/javascript';
script.src = "https://cdn.tiny.cloud/1/on3ip2924chs4ceulp1kxl2br3anol9iieve7cydfxq8ia5j/tinymce/5/tinymce.min.js";
document.head.appendChild(script);

script.onload = function(){

tinymce.init({
    selector: '#id_content',
    height: 656,
    plugins: [
  'advlist autolink link image lists charmap print preview hr anchor pagebreak spellchecker',
  'searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking',
  'table emoticons template paste help'
],
toolbar: 'undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | ' +
  'bullist numlist outdent indent | link image | print preview media fullpage | ' +
  'forecolor backcolor emoticons | help',
menu: {
  favs: {title: 'My Favorites', items: 'code visualaid | searchreplace | spellchecker | emoticons'}
},
menubar: 'favs file edit view insert format tools table help',
content_css: 'css/content.css'
});
}
