<template>
<div class="personal-container">
  <div class="header-wrap">
      <top-Header></top-Header>
  </div>
    <div class="wrap">
      <nav-bar class="nav"></nav-bar>
      <div class="main-container">
        <transition name="fade" mode="out-in">
          <router-view></router-view>
        </transition>
      </div>
    </div>
</div>

</template>
<script>
import navBar from "../components/navbar.vue";
import topHeader from "../components/topheader.vue"
export default {
  components: {
    navBar
  },
}
</script>
<style rel="stylesheet/scss" lang="scss" scoped>
.personal-container{
  padding-top: 74px;
  width: 100%;
  height: 100%;
  background-color: #f4f4f4;
  .el-container {
    margin: 0 auto;
    width: 1170px;
  }
  .nav {
    float: left;
    width: 259px;
    margin-right: 20px;
    box-shadow: 0 2px 4px 0 rgba(210, 210, 210, 0.50);
    border-radius: 4px;
    padding: 20px 0;
    background-color: white;
  }

  .main-container {
        border-radius: 4px;
    background: #FFFFFF;
    box-shadow: 0 2px 4px 0 rgba(210, 210, 210, 0.50);
    border-radius: 4px;
    float: left;
    width: 920px;
    box-sizing: border-box;
    min-height: 420px;
    margin-bottom: 20px;
  }
  .wrap {
        width: 1200px;
    margin: 0px auto;
    position: relative;
  }
  .header-wrap {
    position: relative;
  }

}
</style>
