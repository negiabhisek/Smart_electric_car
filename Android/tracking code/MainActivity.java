package info.androidhive.googlemapsv2;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.util.Log;
import android.widget.Toast;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.CameraPosition;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;

public class MainActivity extends Activity implements Runnable{

	// Google Map
	private GoogleMap googleMap;
	
	GPSTracker gps;
	
	Thread t;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		double latitude;
		double longitude;
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		try {
			// Loading map
			initilizeMap();

			// Changing map type
			googleMap.setMapType(GoogleMap.MAP_TYPE_NORMAL);
			// googleMap.setMapType(GoogleMap.MAP_TYPE_HYBRID);
			// googleMap.setMapType(GoogleMap.MAP_TYPE_SATELLITE);
			// googleMap.setMapType(GoogleMap.MAP_TYPE_TERRAIN);
			// googleMap.setMapType(GoogleMap.MAP_TYPE_NONE);

			// Showing / hiding your current location
			googleMap.setMyLocationEnabled(true);

			// Enable / Disable zooming controls
			googleMap.getUiSettings().setZoomControlsEnabled(true);

			// Enable / Disable my location button
			googleMap.getUiSettings().setMyLocationButtonEnabled(false);

			// Enable / Disable Compass icon
			googleMap.getUiSettings().setCompassEnabled(true);

			// Enable / Disable Rotate gesture
			googleMap.getUiSettings().setRotateGesturesEnabled(true);

			// Enable / Disable zooming functionality
			googleMap.getUiSettings().setZoomGesturesEnabled(true);
			
			// Enable / Disable scroll functionality
			UiSettings.setScrollGesturesEnabled(false)

			// Enable / Disable tilt functionality
			UiSettings.setTiltGesturesEnabled(true)
				
			// update location	
			//locationUpdate(getLocation());
			
			t = new Thread(this, "Update Thread");
			t.start(); // Start the thread

		} catch (Exception e) {
			e.printStackTrace();
		}

	}

	@Override
	protected void onResume() {
		super.onResume();
		initilizeMap();
	}

	/**
	 * function to load map If map is not created it will create it for you
	 * */
	private void initilizeMap() {
		if (googleMap == null) {
			googleMap = ((MapFragment) getFragmentManager().findFragmentById(
					R.id.map)).getMap();

			// check if map is created successfully or not
			if (googleMap == null) {
				Toast.makeText(getApplicationContext(),
						"Sorry! unable to create maps", Toast.LENGTH_SHORT)
						.show();
			}
		}
	}

	/*
	 * getting the current location by using the gps tracker 
	 */
	private double[] getLocationData() 
	{
		//Get GPS data
		gps = new GPSTracker(AndroidGPSTrackingActivity.this);
		
		// create class object
		gps = new GPSTracker(AndroidGPSTrackingActivity.this);

		// check if GPS enabled		
		if(gps.canGetLocation())
		{	
			double latitude = gps.getLatitude();
			double longitude = gps.getLongitude();
			
			// \n is for new line
			Toast.makeText(getApplicationContext(), "Your Location is - \nLat: " + latitude + "\nLong: " + longitude, Toast.LENGTH_LONG).show();	
		}
		else
		{
			// can't get location
			// GPS or Network is not enabled
			// Ask user to enable GPS/network in settings
			gps.showSettingsAlert();
		}
		return new double[] { latitude,longitude };
	}
	
	public void locationUpdate(/*double[] randomLocation location*/)
	{
		double[] randomLocation = getLocationData();
		//double[] randomLocation =location;
		latitude=randomLocation[0];
		longitude = randomLocation[1];
		
		googleMap.addMarker(new MarkerOptions().position(new LatLng(latitude, longitude)).title("Hello Maps"));
		Log.e("Random", "> " + randomLocation[0] + ", "
				+ randomLocation[1]);

		// Move the camera to last position with a zoom level
		CameraPosition cameraPosition = new CameraPosition.Builder().target(new LatLng(randomLocation[0],randomLocation[1])).zoom(15).build();

		googleMap.animateCamera(CameraUpdateFactory.newCameraPosition(cameraPosition));
	}
	
	public void run() 
	{
		try 
		{
			locationUpdate()
			Thread.sleep(10000);
       }
     } catch (InterruptedException e) {
         System.out.println("Child interrupted.");
     }
     
   }
}
