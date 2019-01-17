const calcDistance = function (origin, lat, long) {
  let distanceFromMainTrainstation = origin.distanceTo(L.latLng(lat, long))
  return Number.parseFloat(distanceFromMainTrainstation / 1000).toFixed(2)
}

const navigateTo = function (lat, long) {
  if (!lat || !long) {
    alert("Unfortunately we don't have informationen about the location of this Object!");
  } else {
      if ((navigator.platform.indexOf("iPhone") != -1) || (navigator.platform.indexOf("iPod") != -1) || (navigator.platform.indexOf("iPad") != -1)) {
        window.open(`maps://maps.google.com/maps?daddr=${lat},${long}&amp;ll=`);
    } else {
        window.open(`https://maps.google.com/maps?daddr=${lat},${long}&amp;ll=`)
    }
  }
}

export { calcDistance, navigateTo }
