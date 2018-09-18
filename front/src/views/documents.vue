<template>
  <div class="doc-container">
    <div class="header-wrap">
      <top-Header></top-Header>
    </div>
    <div class="doc-content-container">
       <div class="container">
          <el-tabs v-model="activeName" @tab-click="handleClick">
            <!-- 1 -->
            <el-tab-pane label="快速入门" name="first">
              <div class="my-tabs">
                <div class="tabs-bar tabBar-wrap">
                  <el-menu
                  default-active="1"
                  class="el-menu-vertical-demo"
                  @open="handleOpen">
                  <el-submenu index="1" :class="{'active':this.num == 1}">
                    <template slot="title">
                      <span>简易教程</span>
                    </template>
                    <el-menu-item-group>
                      <el-menu-item index="1-1">
                        <div class="tabs-tab"  :class="{'active':this.num == 1}" @click="tab(1)">第一章</div>
                      </el-menu-item>
                      <el-menu-item index="1-2">
                        <div class="tabs-tab"  :class="{'active':this.num == 2}" @click="tab(2)">第二章</div>
                      </el-menu-item>
                    </el-menu-item-group>
                  </el-submenu>
                  <el-menu-item index="3">
                    <div class="tabs-tab"  :class="{'active':this.num == 3}" @click="tab(3)">开发环境</div>
                  </el-menu-item>
                  <el-menu-item index="4">
                  <div class="tabs-tab"  :class="{'active':this.num == 4}" @click="tab(4)">常见问题</div>
                  </el-menu-item>
                  <el-menu-item index="5">
                  <div class="tabs-tab"  :class="{'active':this.num == 5}" @click="tab(5)">环境部署</div>
                  </el-menu-item>
                </el-menu>
                </div>
                <div class="tabs-content tabsContent-wrap">
                  <div v-show="this.num== 1">这是简易教程的内容11</div>
                  <div v-show="this.num== 2">22</div>
                  <div v-show="this.num== 3">33</div>
                  <div v-show="this.num== 4">44</div>
                  <div v-show="this.num== 5">55</div>
                </div>
              </div>
            </el-tab-pane>
            <!-- 2 -->
            <el-tab-pane label="SDK文档" name="second">
              <div class="my-tabs">
                <div class="tabs-bar tabBar-wrap">
                  <el-menu
                  default-active="1"
                  class="el-menu-vertical-demo"
                  @open="handleOpen">
                  <el-submenu index="1" :class="{'active':this.num == 1}">
                    <template slot="title">
                      <span>简易教程</span>
                    </template>
                    <el-menu-item-group>
                      <el-menu-item index="1-1">
                        <div class="tabs-tab"  :class="{'active':this.num == 1}" @click="tab(1)">第一章</div>
                      </el-menu-item>
                      <el-menu-item index="1-2">
                        <div class="tabs-tab"  :class="{'active':this.num == 2}" @click="tab(2)">第二章</div>
                      </el-menu-item>
                    </el-menu-item-group>
                  </el-submenu>
                  <el-menu-item index="3">
                    <div class="tabs-tab"  :class="{'active':this.num == 3}" @click="tab(3)">开发环境</div>
                  </el-menu-item>
                  <el-menu-item index="4">
                  <div class="tabs-tab"  :class="{'active':this.num == 4}" @click="tab(4)">常见问题</div>
                  </el-menu-item>
                  <el-menu-item index="5">
                  <div class="tabs-tab"  :class="{'active':this.num == 5}" @click="tab(5)">环境部署</div>
                  </el-menu-item>
                </el-menu>
                </div>
                <div class="tabs-content tabsContent-wrap">
                  <div v-show="this.num== 1">这是SDK文档内容111</div>
                  <div v-show="this.num== 2">这是SDK文档内容222</div>
                  <div v-show="this.num== 3">这是SDK文档内容333</div>
                  <div v-show="this.num== 4">这是SDK文档内容444</div>
                  <div v-show="this.num== 5">这是SDK文档内容555</div>
                </div>
              </div>
            </el-tab-pane>
            <!-- 3 -->
            <el-tab-pane label="API文档" name="third">
                <div class="my-tabs">
                <div class="tabs-bar tabBar-wrap">
                  <el-menu
                  default-active="1"
                  class="el-menu-vertical-demo"
                  @open="handleOpen">
                  <el-submenu index="1" :class="{'active':this.num == 1}">
                    <template slot="title">
                      <span>简易教程</span>
                    </template>
                    <el-menu-item-group>
                      <el-menu-item index="1-1">
                        <div class="tabs-tab"  :class="{'active':this.num == 1}" @click="tab(1)">第一章</div>
                      </el-menu-item>
                      <el-menu-item index="1-2">
                        <div class="tabs-tab"  :class="{'active':this.num == 2}" @click="tab(2)">第二章</div>
                      </el-menu-item>
                    </el-menu-item-group>
                  </el-submenu>
                  <el-menu-item index="3">
                    <div class="tabs-tab"  :class="{'active':this.num == 3}" @click="tab(3)">开发环境</div>
                  </el-menu-item>
                  <el-menu-item index="4">
                  <div class="tabs-tab"  :class="{'active':this.num == 4}" @click="tab(4)">常见问题</div>
                  </el-menu-item>
                  <el-menu-item index="5">
                  <div class="tabs-tab"  :class="{'active':this.num == 5}" @click="tab(5)">环境部署</div>
                  </el-menu-item>
                </el-menu>
                </div>
                <div class="tabs-content tabsContent-wrap">
                  <div v-show="this.num== 1">这是API文档的内容111</div>
                  <div v-show="this.num== 2">这是API文档的内容222</div>
                  <div v-show="this.num== 3">这是API文档的内容333</div>
                  <div v-show="this.num== 4">这是API文档的内容444</div>
                  <div v-show="this.num== 5">这是API文档的内容555</div>
                </div>
              </div>
            </el-tab-pane>
            <!-- 4 -->
            <el-tab-pane label="研发动态" name="fourth">
              <div class="my-tabs">
                <div class="tabs-bar tabBar-wrap">
                  <el-menu
                  default-active="1"
                  class="el-menu-vertical-demo"
                  @open="handleOpen">
                  <el-submenu index="1" :class="{'active':this.num == 1}">
                    <template slot="title">
                      <span>简易教程</span>
                    </template>
                    <el-menu-item-group>
                      <el-menu-item index="1-1">
                        <div class="tabs-tab"  :class="{'active':this.num == 1}" @click="tab(1)">第一章</div>
                      </el-menu-item>
                      <el-menu-item index="1-2">
                        <div class="tabs-tab"  :class="{'active':this.num == 2}" @click="tab(2)">第二章</div>
                      </el-menu-item>
                    </el-menu-item-group>
                  </el-submenu>
                  <el-menu-item index="3">
                    <div class="tabs-tab"  :class="{'active':this.num == 3}" @click="tab(3)">开发环境</div>
                  </el-menu-item>
                  <el-menu-item index="4">
                  <div class="tabs-tab"  :class="{'active':this.num == 4}" @click="tab(4)">常见问题</div>
                  </el-menu-item>
                  <el-menu-item index="5">
                  <div class="tabs-tab"  :class="{'active':this.num == 5}" @click="tab(5)">环境部署</div>
                  </el-menu-item>
                </el-menu>
                </div>
                <div class="tabs-content tabsContent-wrap">
                  <div v-show="this.num== 1">这是研发动态的内容111</div>
                  <div v-show="this.num== 2">这是研发动态的内容222</div>
                  <div v-show="this.num== 3">这是研发动态的内容333</div>
                  <div v-show="this.num== 4">这是研发动态的内容444</div>
                  <div v-show="this.num== 5">这是研发动态的内容555</div>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "document",
  data() {
    return {
      num: 1,
      activeName: 'first'
    }
  },
  methods: {
    tab(index) {
      this.num = index;
    },
    handleOpen(key, keyPath) {
        this.tab(key);
    },
     handleClick(tab, event) {
       this.num = 1;
      }
  }
};
</script>
<style rel="stylesheet/scss" lang="scss">
.doc-container{
  background: #fff;
  min-height: 1000px;
  .doc-content-container{
    padding-top: 55px;
  }
  .container{
    width: 1200px;
    margin: 0 auto;
  }
  // 切换
  .el-tabs__header{
    padding-left: 282px;
  }
  .el-tabs__item{
    padding: 0 40px;
    height: 76px;
    line-height: 76px;
    font-size: 16px;
    color: #A9A9B3;
    text-align: center;
  }
  .el-tabs--top .el-tabs__item.is-top:last-child {
    padding: 0 20px 0 40px;
  }
  .el-tabs--top .el-tabs__item.is-top:nth-child(2){
    padding: 0 40px 0 20px;
  }
  .el-tabs__active-bar{
      background-color: #4F81F4;
  }
  .el-tabs__item.is-active{
      font-size: 18px;
      color: #444444;
  }
  .el-tabs__nav-wrap::after{
    height: 1px;
    background-color: #eeeeee;
  }
  .tabBar-wrap{
    width: 180px;
    background: #fff;
    display: inline-block;
  }
  .el-menu{
    border: none;
  }
  .el-submenu__title,.el-menu-item{
    font-size: 16px;
    color: #A9A9B3;
    border-bottom: 1px solid #eeeeee;
  }
  .el-submenu__title:hover {
     background-color: #4F81F4;
     font-size: 16px;
     color: #FFFFFF;
  }
 .el-menu-item:focus, .el-menu-item:hover {
     background-color: #4F81F4;
     font-size: 16px;
     color: #FFFFFF;
  }
  .el-submenu.is-active .el-submenu__title {
     background-color: #4F81F4;
     font-size: 16px;
     color: #FFFFFF;
     border: none
  }
  .el-submenu__title:hover .el-submenu__icon-arrow {
    color: #FFFFFF;
  }
  .el-submenu__title i:hover{
    color: #FFFFFF;
  }
  .el-submenu.is-active .el-submenu__title i {
     color: #FFFFFF;
  }
  .el-submenu .el-menu-item {
      height: 50px;
      line-height: 50px;
      padding: 0 45px;
      min-width: 180px;
  }
  .active .el-submenu__title {
    background-color: #4F81F4;
     font-size: 16px;
     color: #FFFFFF;
  }
  .active .el-submenu__icon-arrow{
     color: #FFFFFF;
  }
  .tabsContent-wrap{
    display: inline-block;
    float: right;
    width: 76%;
    margin: 0 auto;
    padding-left: 102px;
  }
}
</style>
