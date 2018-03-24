function query_data_compare_function() {
    var options=$("#compare_settings_list option:selected");
    data={
        settings_id:options.val()
    };
    url="./sample_compare_query_data";
    $.ajax({
        url:url,
        type:"POST",
        cache:false,
        async:true,
        data:data,
        timeout: 60 * 1000,
        success:function (result) {
            // alert("当前批次:"+options.text()+"\n"+"fpm_in:总group："+result.result_db1.Count_sum+",已完成："+result.result_db1.is_complete+",未完成："+result.result_db1.is_not_complete+"\n"
            //     +"fpm_out:总group："+result.result_db2.Count_sum+",已完成："+result.result_db2.is_complete+",未完成："+result.result_db2.is_not_complete+"\n");
            console.log(result);
            result_str ="当前批次："+options.text()+"\n";
            for (var i in  result['result']){
                item = result['result'][i];
                console.log(item['db']);
                temp_str = ""+item['db']+"\n"
                    +"总group个数:"+item['Count_sum']+"\n"
                    +"已完成个数："+item['is_complete']+"\n"
                    +"未完成个数："+item['is_not_complete']+"\n"
                    +"================="+"\n";
                result_str +=temp_str
            }
            alert(result_str);

        }
    });

}
