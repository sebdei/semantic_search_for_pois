<template>
  <div class="text-wrapper d-flex">
    <div class="icon">
      <span class="fa-stack fa-2x">
        <i class="fas fa-ellipsis-h fa-stack-1x"></i>
        <i class="far fa-comment-alt fa-stack-2x"></i>
      </span>
    </div>

    <transition name="fade">
      <div v-if="active">
        <div class="content">
          <div>
            <textarea placeholder="Your custom text" v-model="query"></textarea>
          </div>
          <div class="submit-button" @click="submitQuery">
            <div class="">
              <i class="fas fa-arrow-circle-right fa-1x"></i>
            </div>
          </div>
        </div>
        <div class="back-button" @click="deactivate">
          <i class="fas fa-chevron-left fa-2x"></i>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  props: ['active'],
  data () {
    return {
      query: 'test'
    }
  },
  methods: {
    deactivate: function () {
      this.$emit('deactivate')
    },
    submitQuery: async function () {
      let postData = { query: this.query }
      let host = window.location.hostname;
      let response = await axios.post(`http://${host}:5001/classify`, { query: this.query })
      this.results = response.data
    }
  }
}
</script>

<style scoped>
.text-wrapper {
  background-color: #A39A92;
  height: 100%;
}
.icon {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  left: 50px;
}

.content {
  position: absolute;
  top: 50%;
  right: 10%;
  transform: translateY(-50%);
  color: white;
}

textarea {
  max-height: 90%;
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
  background: #77685D;
  resize: vertical;
  color: white;
}

textarea::placeholder {
  color: white;
}

textarea::before {
  content: '';
  display: table;
}

textarea::after {
  content: '';
  display: table;
  clear: both;
}

.submit-button {
  text-align: right;
  font-size: 1.4em;
}

.back-button {
  position: absolute;
  top: 5px;
  left: 5px;
  padding: 15px;
  font-size: 1.4em;
}

.back-button i {
  font-size: 1.3em;
}

.fade-enter-active {
  transition: opacity 4s;
}

 .fade-leave-active {
   transition: opacity 1s;
 }

.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
