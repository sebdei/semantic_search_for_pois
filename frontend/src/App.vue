<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import Word2VecTest from './components/Word2VecTest.vue'

export default {
  name: 'app',
  components: {
    Word2VecTest
  }
}
</script>

<style>
body {
  overflow-x: hidden;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
