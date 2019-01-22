<template>
  <div class="twitter-wrapper d-flex">
    <div class="icon">
      <i class="fab fa-4x fa-twitter"></i>
    </div>

    <transition name="fade">
      <div v-if="active">
        <div class="content">
          <h5>Your Twitter name</h5>
          <form @submit.prevent="submit">
            <input v-model="twitterName" />
          </form>
        </div>
        <div class="back-button" @click="deactivate">
          <i class="fas fa-chevron-right fa-2x"></i>
        </div>
      </div>
    </transition>

  </div>
</template>

<script>
import axios from 'axios'

import { L } from 'vue2-leaflet'
import { setCookie } from '@/service/cookie-service'

export default {
  props: ['active'],
  data () {
    return {
      twitterName: ''
    }
  },
  methods: {
    deactivate: function () {
      this.$emit('deactivate')
    },
    submit: async function () {
      let host = window.location.hostname
      let response = await axios.post(`http://${host}:5000/users/create_user_with_twitter_name/`, { 'twitter_name': this.twitterName })

      // for simplicity reasons the cookie is set by manually
      let userId = response.data.cookie.user_id
      setCookie('user_id', userId)
    }
  }
}
</script>

<style scoped>
.twitter-wrapper {
  background-color: #00aced;
  height: 100%;
}
.icon {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  right: 50px;
  color: white;
}

.content {
    position: absolute;
    top: 50%;
    left: 10%;
    transform: translateY(-50%);
    color: white;
}

input {
  width: auto;
  border-radius: 4px;
  box-shadow: 0 40px 50px rgba(0,0,0,0.25);
  font-size: 1em;
  outline: none;
  border: 0;
  padding: 8px;
  background: white;
  outline: none;
  width: auto;
  border: 0;
  padding: 8px;
  background: white;
}
input::before {
  content: '';
  display: table;
}
input::after {
  content: '';
  display: table;
  clear: both;
}

.back-button {
  position: absolute;
  top: 5px;
  right: 5px;
  padding: 15px;
  font-size: 1.4em;
  color: white;
}

.back-button i {
  font-size: 1.3em;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 4s;
}
.fade-leave-active {
  transition: opacity 0.1s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
