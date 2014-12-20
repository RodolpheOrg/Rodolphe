{% load i18n %}
function quote_post(url) {
    textarea = "textarea#id_content";
    content = $(textarea).val();
    if (content)
	content += "\r\n";
    $.getJSON(url, function(post) {
	content += "&#" + post.id + " **" + post.author + "** " + '{% trans "wrote" %}' + "\r\n";
	$.each(post.content.split("\r\n"), function(i, line) {
            content += "> " + line + "\r\n";
	});
	content += "\r\n";
	$(textarea).val(content);
    });
}

function post_preview() {
    text = $("#post_form #id_content").val();
    $("#post_preview p.content").load("/render", {"content": text});
    $("#post_preview").show();
}
