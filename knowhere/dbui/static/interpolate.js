
function interpolate(timestamp,deltach0) {
  var itrtime = [];
  var itrdata =[];

  for (var i = 0; i < timestamp.length-1; i++) {
    var dtime = timestamp[i+1] - timestamp[i];
    var step = (deltach0[i+1] - deltach0[i])/dtime;

    for (var j = 0; j <= dtime; j++) {
      var temp_time = Number(timestamp[i])+Number(j);
       itrtime.push(temp_time);
       var gadge = (j*step)
      var temp_ch0 = Number(deltach0[i])+ Number(gadge);
       itrdata.push(temp_ch0);
      }
    }
    console.log(itrtime);
    return [itrtime,itrdata];
}
