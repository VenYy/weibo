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

chart1()