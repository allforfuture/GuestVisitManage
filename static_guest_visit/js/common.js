//打开登录窗口
function openLoginWindow(){
    layer.open({
        type:1,
        title:'登录',
        area:['350px','211px'],
        resize:false,
        content:'<div class="layui-form-item">' +
                    '<div class="layui-inline" style="margin-top:10px">' +
                      '<label class="layui-form-label">请输入工号:</label>' +
                      '<div class="layui-input-inline">' +
                        '<input type="text" id="usernum" autocomplete="off" class="layui-input" autofocus="autofocus">' +
                      '</div><span class="redinput">*</span>' +
                    '</div>' +
                    '<div class="layui-inline">' +
                      '<label class="layui-form-label">请输入密码:</label>' +
                      '<div class="layui-input-inline">' +
                        '<input type="password" id="password" autocomplete="off" class="layui-input">' +
                      '</div><span class="redinput">*</span>' +
                    '</div>' +
                    '<hr/>' +
                    '<div class="layui-row">' +
                        '<div class="btn layui-bg-green tc layui-col-sm-offset4 layui-col-sm3 layui-btn-sm" onclick="login(this)">登录</div>' +
                        '<div class="btn layui-btn-primary tc layui-col-sm3 layui-col-sm-offset1 layui-btn-sm" onclick="cancel()">取消</div>' +
                    '</div>' +
                '</div>'
    });
}

//执行登录操作
function login(obj){
    var usernum = $("#usernum").val()
    var password = $("#password").val()
    var csrf_token = $("#csrf_token").val()
    data = {usernum:usernum,password:password,'csrfmiddlewaretoken': csrf_token}

    if(usernum == '' || password == ''){
        layer.alert('用户名和密码不能为空！',{title:'温馨提示',icon:7})
        return
    }

    $.ajax({
        url:'login',
        type:'post',
        data:data,
        dataType:'json',
        success:function(data){
            if(data.result){    //登录成功
                $("#user_id").val(data.user_id)
                $("#role_text").val(data.role_text)
                $("#user_name").text(data.user_name)
                $("#usershow").removeClass('hide')
                $("#loginwindow").addClass('hide')

                $(".layui-layer-close1").click()   //关闭登录界面
                layer.msg('登录成功')

            }else{              //登录失败
                layer.alert(data.msg,{title:'温馨提示',icon:2})
            }
        },
        error:function(xmlHq,status,errorThrows){
            alert(errorThrows)
        }
    })
}

//取消登录
function cancel(){
    $(".layui-layer-close1").click()
}

//注销
function logout(){
    $.ajax({
        url:'/logout',
        type:'get',
        dataType:'json',
        success:function(data){
            if(data.result){
                $("#usershow").addClass('hide')
                $("#user_id").val('')
                $("#role_text").val('')
                $("#user_name").text('')
                layer.msg('注销成功，正在前往登录页...')
                window.setTimeout(function(){
                    window.location.href = "/login_page"
                    //window.location.reload()
                },3000)
            }else{
                layer.alert('注销失败，请检查网络或联系管理员',{title:'温馨提示',icon:5})
            }
        },
        error:function(xmlHq,status,errorThrows){
            console.log(errorThrows)
            window.location.href = "/login_page"
        }
    })
}

//身份验证输入框获取焦点是弹出提示信息
function show_identify_tips(obj){
  layer.tips("身份证、护照、港澳通行证、居住证亦可。", $(obj), {
    tips: [3, '#3595CC'],
    area: ['260px', 'auto'],
    time: 3000
  });
}

//判断输入框是否为空
function isnull_tip_msg(msg,obj){
  $(obj).addClass('bor_red');
  //$(obj).focus();
  layer.tips(msg, $(obj), {
    tips: [3, '#F00'],
    area: ['190px', 'auto'],
    time: 3000
  });
}

//获取今天的日期
function get_today(){
    let date = new Date()
    let year = date.getFullYear()
    let month = date.getMonth() + 1
    if(month < 10){
        month = '0' + month
    }
    let day = date.getDate()
    if(day < 10){
        day = '0' + day
    }
    return year + '-' + month + '-' + day
}