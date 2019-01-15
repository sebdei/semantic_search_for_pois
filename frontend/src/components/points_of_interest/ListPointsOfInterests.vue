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
        <div class="distance-box float-right" @click="navigateTo(recommendation.lat, recommendation.long)">
          <div>
            <i class="fas fa-map-marker-alt"></i>
          </div>
          <span>
            40.2 km
          </span>
        </div>
        <div class="teaser-text">
          Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam        </div>
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
  background-color: #8E7876;
  height: 180px;
  padding: 30px;
}

.poi-item:nth-child(even) {
  background-color: #463E3C;
}

.street {
  display: inline-block;
  width: 75%;
}

.distance-box {
  display: inline-block;
  padding: 5px;
  text-align: center;
  background-color: #79A8AF;
  border-radius: 10px;
}

.teaser-text {
  /* max-height: 70px;
  overflow:hidden;
  text-overflow: ellipsis;
  position: relative;
  text-align: justify; */

  display: -webkit-box;
  max-width: 75%;
  height: 55px;
  line-height: 1.2;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

</style>
