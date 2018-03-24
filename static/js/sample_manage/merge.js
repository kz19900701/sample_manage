function query_data_function() {
    var options=$("#merge_settings_list option:selected");
    // alert(options.val())
    // alert(options.text())
    data={
        settings_id:options.val()
    };
    url="./sample_merge_query_data";
    $.ajax({
        url:url,
        type:"POST",
        cache:false,
        async:true,
        data:data,
        timeout: 60 * 1000,
        success:function (result) {
            alert("当前批次:"+options.text()+"\n"+"result_combine 总数："+result.result_db1.Count_sum+",已合并："+result.result_db1.is_complete+",未合并："+result.result_db1.is_not_complete+"\n"
                +"double_check 总数："+result.result_db2.Count_sum+",已标注："+result.result_db2.is_complete+",未标注："+result.result_db2.is_not_complete+"\n");
        }
    });

}
function query_data_function2() {
    var options=$("#download_settings_list option:selected");
    // alert(options.val())
    // alert(options.text())
    data={
        settings_id:options.val()
    };
    url="./sample_merge_query_data";
    $.ajax({
        url:url,
        type:"POST",
        cache:false,
        async:true,
        data:data,
        timeout: 60 * 1000,
        success:function (result) {
            alert("当前批次:"+options.text()+"\n"+"result_combine 总数："+result.result_db1.Count_sum+",已合并："+result.result_db1.is_complete+",未合并："+result.result_db1.is_not_complete+"\n"
                +"double_check 总数："+result.result_db2.Count_sum+",已标注："+result.result_db2.is_complete+",未标注："+result.result_db2.is_not_complete+"\n");
        }
    });

}

function query_data_function3() {
    var options=$("#stat_settings_list option:selected");
    // alert(options.val())
    // alert(options.text())
    data={
        settings_id:options.val()
    };
    url="./sample_merge_query_data";
    $.ajax({
        url:url,
        type:"POST",
        cache:false,
        async:true,
        data:data,
        timeout: 60 * 1000,
        success:function (result) {
            alert("当前批次:"+options.text()+"\n"+"result_combine 总数："+result.result_db1.Count_sum+",已合并："+result.result_db1.is_complete+",未合并："+result.result_db1.is_not_complete+"\n"
                +"double_check 总数："+result.result_db2.Count_sum+",已标注："+result.result_db2.is_complete+",未标注："+result.result_db2.is_not_complete+"\n");
        }
    });

}