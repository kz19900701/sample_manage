function test_entity() {
    url = "/test_app_entity";
    var input_content =  $('#input_content').val();
    data = {
        input_content:input_content
    }
    $.ajax({
           type: "POST",
           cache:false,
           async : true,
           url:  url,
           data:data,
           success: function(dic) {
                 alert("企业实体识别："+dic.result );
           }})
}

function test_yuqing() {
    url = "/test_app_yuqing";
    var input_content =  $('#input_content').val();
    data = {
        input_content:input_content
    }
    $.ajax({
           type: "POST",
           cache:false,
           async : true,
           url:  url,
           data:data,
           success: function(dic) {
                 alert("舆情分类："+dic.result );
           }})
}
function test_susong() {
    url = "/test_app_susong";
    var input_content =  $('#input_content').val();
    data = {
        input_content:input_content
    }
    $.ajax({
           type: "POST",
           cache:false,
           async : true,
           url:  url,
           data:data,
           success: function(dic) {
                 alert("诉讼分类："+dic.result );
           }})
}