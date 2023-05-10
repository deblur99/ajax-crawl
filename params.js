function searchBusStationJson() {
    var url = "/gbis2014/schBusAPI.action";
    var data = "cmd=searchRealBusStationJson";
    data += "&stationId=" + stationId;
    data += "&routeId=" + routeId;

    $.ajax({
        type: "post",
        contentType: "application/x-www-form-urlencoded;charset=UTF-8",
        dataType: "json",
        url: url,
        data: data,
        success: searchBusStationJsonSuccess,
        error: ajaxError,
    });
}
