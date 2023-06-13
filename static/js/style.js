function chart1() {
    var chart = echarts.init(document.getElementById("chart1"), {renderer: "canvas"})
    $.ajax({
        type: "GET",
        url: "/chartApi/chart1",
        dataType: "json",
        success: function (data) {
            console.log("success")
            chart.setOption(data)
        },
        error: function (e) {
            console.log(e)
        }
    })

}
function chart2() {
    var chart = echarts.init(document.getElementById("chart2"), {renderer: "canvas"})
    $.ajax({
        type: "GET",
        url: "/chartApi/chart2",
        dataType: "json",
        success: function (data) {
            console.log("success chart2")
            chart.setOption(data)
        }
    })
}


chart1()
chart2()

// 遍历每个带有 data-hot 属性的 td 元素
$('td[data-hot]').each(function() {
  // 获取 data-hot 的值，并将其转换为整数
  const hotValue = parseInt($(this).attr('data-hot'));

  // 如果 data-hot 的值大于 1000，给该行中的第一个 td 元素添加 hot 类名
  if (hotValue > 1000) {
    $(this).closest('tr').find('td:first-child').addClass('hot');
  }
});



