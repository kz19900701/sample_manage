function sample_upload() {
    var name = $('input[name="name"]').val();
    var settings = $('input[name="settings"]').val();
    var setting_type = $('input[name="setting_type"]').val();
    var upload_file = $('input[name="upload_file"]').val();
    data={
        name:name,
        settings:settings,
        setting_type:setting_type
    };
    var url = "./sample_upload_api";
    $.ajax({
           type: "POST",
           cache:false,
           async : true,
           url:  url,
           data:data,
           timeout: 60 * 1000,
           success: function(dic) {
                 alert("数据：" + dic.result );
           }})
}