<template>
  <div id="app" v-cloak>
      <router-view/>
  </div>
</template>

<script>
  // import topHeader from "./components/topheader.vue";
  // import { getQueryList, search } from "@/api/api";
  export default {
    name: "App",
    data() {
      return {
        isRouterAlive: true
      };
    }
  };
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style rel="stylesheet/scss" lang="css" scoped>
  #app {
    height: 100%;
  }
</style>
