max = 1000
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
                moments = cv2.moments(cnt)
                if moments['m00'] > max:
			max = moments['m00']
                        x = int(moments['m10']/moments['m00'])
                        y = int(moments['m01']/moments['m00'])
                        cv2.drawContours(display, cnt,1, (0,255,0), 1)
                        cv2.circle(display, (x,y),int(math.sqrt(moments['m00']/math.pi)), red,-1)
                        cv2.circle(display, (x,y),5,blue,-1)
			largest = max

 
