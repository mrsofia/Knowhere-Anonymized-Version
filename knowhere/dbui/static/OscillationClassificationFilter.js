// OscillationFilter Function ----------------------------------
function OscillationClassificationFilter(frame,timeStamp)
{
    var input_list = frame;
    this.frame = frame

      var initThreshold       = 30000
      var activationThreshold = 50000
      var oscillationWindow   = 100
      var numOscillation      = 4
      var upperThreshold      = 80000
      var lowerThreshold      = 10000

      var upper_averageAbsPower     = 0
      var upper_sumPower            = 0
      var upper_frameBufferSize    = 10

      var lower_averageAbsPower     = 0
      var lower_sumPower            = 0
      var lower_frameBufferSize    = 15

     this.setThresholds= function(initT,actT,upper,lower,oscW,numO,UFB_Size,LFB_Size)
     //,FB_Size,iniT,actT,oscWindow,numOsc
      {
        initThreshold       = initT
        upperThreshold      = upper
        lowerThreshold      = lower
        activationThreshold = actT

        oscillationWindow   = oscW
        numOscillation      = numO
        upper_frameBufferSize     = UFB_Size
        lower_frameBufferSize     = LFB_Size
        upper_filterBuffer=[];
        lower_filterBuffer=[];
      }

    this.consume = function(currentlyActivating,current_state,current_riseFlag,current_fallFlag,current_startTime,
      current_oCounter,current_timeStamp,upper_filterBuffer,lower_filterBuffer)

      {

        return classify(frame,currentlyActivating,current_state,current_riseFlag,current_fallFlag,current_startTime,
          current_oCounter,current_timeStamp,upper_filterBuffer,lower_filterBuffer)
      }

    var updateBuffer = function(frame,upper_filterBuffer,lower_filterBuffer)
    {
      upper_filterBuffer.push(frame)
      if (upper_filterBuffer.length > upper_frameBufferSize )
      {
        upper_filterBuffer.shift();

      }
      lower_filterBuffer.push(frame)
      if (lower_filterBuffer.length > lower_frameBufferSize )
      {
        lower_filterBuffer.shift();

      }

    }

    var classify = function(frame,currentlyActivating,current_state,current_riseFlag,current_fallFlag,current_startTime,
      current_oCounter,timeStamp,upper_filterBuffer,lower_filterBuffer)
    {


      var initState = current_state;
      var riseFlag  = current_riseFlag;
      var fallFlag  = current_fallFlag;
      var startTime = current_startTime;
      var oCounter  = current_oCounter;
      var currentlyActivating = currentlyActivating;

      var deltaADC1 = frame
      var lastUpdate = timeStamp
	  
	  if (initState ==2 )
      {

        for(i=0;i<upper_filterBuffer.length;i++)
        {
            upper_sumPower += Math.abs(upper_filterBuffer[i])
          //  console.log(sumPower);
        }

        for(i=0;i<lower_filterBuffer.length;i++)
        {
            lower_sumPower += Math.abs(lower_filterBuffer[i])
        }

        lower_averageAbsPower = lower_sumPower/(lower_filterBuffer.length)
        upper_averageAbsPower = upper_sumPower/(upper_filterBuffer.length)


        if(upper_averageAbsPower > upperThreshold)
        {
          //console.log("we catched a true activation");
          //console.log(upper_averageAbsPower);
        //  console.log(upper_filterBuffer.length);
            currentlyActivating   = true
            upper_averageAbsPower = 0
            upper_sumPower        = 0
            lower_averageAbsPower = 0
            lower_sumPower        = 0

        }
        else if(lower_averageAbsPower < lowerThreshold)
        {
            // console.log('enter 9...'+initState);
            // console.log(filterBuffer);
            // console.log("lowerThreshold hit");
            // console.log(frame);
            currentlyActivating = false
            upper_averageAbsPower = 0
            upper_sumPower        = 0
            lower_averageAbsPower = 0
            lower_sumPower        = 0
			initState = 3;
        }

      }else if(initState == 1)
	  {
		  if (lastUpdate - startTime < oscillationWindow)
		  {
			  if(riseFlag ==1 && deltaADC1 <= (-1*(activationThreshold)))
			  {
		  
					  startTime = lastUpdate;
					  riseFlag  = 0;
					  fallFlag  = 1;
					  if (oCounter>=numOscillation)
					  {

						initState = 2;
						oCounter  = 0;
						riseFlag  = 0;
						fallFlag  = 0;
					  }
					  oCounter++;
					
				  
			  }else if(fallFlag == 1 && deltaADC1 >= activationThreshold)
			  {
			  
					  startTime = lastUpdate;
					  riseFlag  = 0;
					  fallFlag  = 1;
					  if (oCounter>=numOscillation)
					  {
						initState = 2;
						oCounter  = 0;
						riseFlag  = 0;
						fallFlag  = 0;
					  }
					  oCounter++;
					
			  }
			  
		  }else
			{
				initState = 3;
				oCounter  = 0;
			}
		  
		  
	  }else if(initState == 0)
	  {
		if(deltaADC1 >= initThreshold)
		{
			initState = 1
			riseFlag  = 1
			fallFlag = 0
			startTime = lastUpdate
		}else if(deltaADC1 <= (-1*(initThreshold)))
		{
			initState = 1
            fallFlag  = 1
		    riseFlag = 0
            startTime = lastUpdate
		}
		  
	  }else if(initState == 3)
	  {
		  	initState = 0
            fallFlag  = 0
		    riseFlag = 0
	  }
	  



      // console.log(".//..."+lower_averageAbsPower);
      updateBuffer(frame,upper_filterBuffer,lower_filterBuffer)
        // console.log("./////..."+lower_averageAbsPower);
      // console.log(currentlyActivating);
      return [currentlyActivating,initState,riseFlag,fallFlag,startTime,oCounter,timeStamp,upper_filterBuffer,lower_filterBuffer];

    }

}
