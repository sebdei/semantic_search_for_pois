<template>
  <div>
    <div class="header pt-5">
      <h2 class="header-text text-center">
        Your personal recommendations
      </h2>
    </div>
    <div class="poi-list">
      <div v-for="(recommendation, index) in listOfRecommendations" class="poi-item">
        <h5 class="font-weight-bold">
          {{ recommendation.name }}
        </h5>
        <div class="street font-weight-bold">
          {{ recommendation.street_name }} {{ recommendation.street_number }}
        </div>
        <div class="teaser-text-wrapper">
          <div class="teaser-text">
            Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam
          </div>
        </div>
        <div class="distance-box float-right" @click="navigateTo(recommendation.lat, recommendation.long)">
          <div>
            <i class="fas fa-map-marker-alt"></i>
          </div>
          <span>
            40.2 km
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      listOfRecommendations: []
    }
  },
  mounted () {
    this.fetchRecommendations()
  },
  methods: {
    fetchRecommendations: async function () {
      let query = 'art museum'

      let host = window.location.hostname
      let response = await axios.post(`http://${host}:5000/classify`, { query: query })
      this.listOfRecommendations = response.data
      console.log(response.data)
    },
    navigateTo: function (lat, long) {
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
  }
}
</script>

<style scoped>
.header {
  height: 150px;
  background-color: #463E3C;
  color: white;
}

.poi-list {

}

.poi-item {
  background-color: #766d6c;
  min-height: 180px;
  padding: 30px;
  border-top: 1px solid;
}

.poi-item:nth-child(even) {
  /* background-color: #463E3C; */
}

.street {
  display: inline-block;
  width: 75%;
}

.distance-box {
  display: inline-block;
  padding: 5px;
  text-align: center;
  border-radius: 7px;
  border: 1px solid rgba(0,0,0,0.23);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
}

.teaser-text {
  display: -webkit-box;
  height: 55px;
  line-height: 1.2;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.teaser-text-wrapper {
  display: inline-block;
  width: 75%;
}
</style>
