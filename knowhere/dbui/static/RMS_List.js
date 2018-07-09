function calculate_rms(list_ch0,stride)
{
  var array     = [];
  var rms_array = [];


  for (var i = 0; i < stride; i++)
  {
    var value =list_ch0[i];
    array.push(value);
    var rms = root_mean_square(array);
    rms_array.push(rms);
  }
  for (var i = stride; i < list_ch0.length; i++)
  {
    array.shift();
    var value =list_ch0[i];
    array.push(value);
    var rms = root_mean_square(array);
    rms_array.push(rms);
  }

  return rms_array;
};

function root_mean_square(ary)
{
  var sum_of_squares = ary.reduce(function(s,x) {return (s + x*x)}, 0);
  return Math.sqrt(sum_of_squares / ary.length);
}
