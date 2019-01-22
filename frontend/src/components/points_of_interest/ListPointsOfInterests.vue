<template>
  <div>
    <div class="header pt-5">
      <h2 class="header-text text-center">
        Your personal recommendations
      </h2>
    </div>
    <div class="poi-list">
      <div v-for="recommendation in listOfRecommendations" class="poi-item" @click="goToDetailPoiRoute(recommendation.id)" :key="recommendation.id">
        <h5 class="font-weight-bold">
          {{ recommendation.name }}
        </h5>
        <div class="teaser-text-wrapper">
          <div class="teaser-text">
            {{ recommendation.source.text }}
          </div>
        </div>
        <div class="distance-box float-right" @click="navigateTo(recommendation.lat, recommendation.long)">
          <div>
            <i class="fas fa-map-marker-alt fa-icon"></i>
          </div>
          <span>
            {{ recommendation.distance}} km
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

import { L } from 'vue2-leaflet';
import { calcDistance, navigateTo } from '@/service/osm-service'
import { getCookie } from '@/service/cookie-service'

export default {
  data () {
    return {
      berlinMainTrainstationLeaflet: L.latLng(52.525084, 13.369402), // for demo purpose: use berlin station as start point
      listOfRecommendations: []
    }
  },
  mounted () {
    if (!getCookie('user_id')) {
      this.$router.push({ path: `/` })
    } else {
      this.fetchRecommendations()
    }
  },
  methods: {
    fetchRecommendations: async function () {
      let host = window.location.hostname
      let queryParam = {
        forceBadWeather: false,
        lat: 52.525084,
        long: 13.369402,
        radius: 2,
        weatherAPI: false,
        userId: getCookie('user_id')
      }

      let response = await axios.get(`http://${host}:5000/points_of_interests/personal_recommendations/`+
        `${queryParam.userId}/${queryParam.lat}/${queryParam.long}/${queryParam.radius}`)
      // let response = await axios.get(`http://${host}:5000/points_of_interests`)
      let listOfRecommendations = response.data

      this.listOfRecommendations = listOfRecommendations.map((recommendation) => {
        recommendation.distance = calcDistance(this.berlinMainTrainstationLeaflet, recommendation.lat, recommendation.long)
        return recommendation
      })
    },
    goToDetailPoiRoute: function (id) {
      this.$router.push({ path: `/points_of_interests/${id}` })
    },
    navigateTo: navigateTo
  }
}
</script>

<style scoped>
.header {
  height: 150px;
  background-color: #463E3C;
  color: white;
}

.poi-item {
  /* background-color: #766d6c; */
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
  font-family: "Droid Serif";
  display: -webkit-box;
  height: 78px;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 14px;
  font-style: normal;
  font-variant: normal;
  line-height: 20px;
  text-align: justify;
}

.teaser-text-wrapper {
  display: inline-block;
  width: 75%;
}

.fa-icon{
  color: #e44802
}
</style>
