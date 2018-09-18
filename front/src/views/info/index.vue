<template>
  <el-row :gutter="20">
    <el-col :span="4">
      <div class="grid-content"></div>
    </el-col>
    <el-col :span="16">
      <div class="grid-content list-home bg-purple">
        <div class="list-header">
          <h3>Ulord博客</h3>
          <a class="mc info" @click.prevent.native="logOut">登出</a>
          <router-link to="/" class="mc publish">返回主页</router-link>
        </div>
        <div class="list-content" v-if="loading">
          <el-tabs v-model="activeName" @tab-click="handleClick">
            <el-tab-pane label="发布的文章" name="first">
              <div class="item" v-for="item in data.msg.publish" :key="item.index">
                <h4 class="item-title">
                  {{item.title || '暂无'}}
                  <span v-if="item.type ==2 " class="abc">广告</span>
                  <span v-if="item.udfs" class="abc">已购买</span>
                </h4>
                <div class="item-main">
                  <p class="intro">
                    {{item.description || '暂无'}} </p>
                </div>
                <div class="price">{{item.price || '暂无'}}SUT</div>
                <div class="author">发布地址：{{item.author || '暂无'}}</div>
                <div class="more" @click="renewal(item.claim_id)">
                  广告续费
                </div>
                <div class="more" @click="goDetail(item.udfs, item.claim_id, item.author, item.price)">
                  查看更多
                </div>
              </div>
            </el-tab-pane>
            <el-tab-pane label="购买的文章" name="second">
              <div class="item" v-for="item in data.msg.order" :key="item.index">
                <h4 class="item-title">
                  {{item.title || '暂无'}}
                  <span v-if="item.type ==2 " class="abc">广告</span>
                  <span v-if="item.udfs" class="abc">已购买</span>
                </h4>
                <div class="item-main">
                  <p class="intro">
                    {{item.description || '暂无'}} </p>
                </div>
                <div class="price">{{item.price || '暂无'}}SUT</div>
                <div class="author">发布地址：{{item.author || '暂无'}}</div>
                <div class="more" @click="goDetail(item.udfs, item.claim_id, item.author, item.price)">
                  查看更多
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </div>
    </el-col>
    <el-col :span="4">
      <div class="grid-content"></div>
    </el-col>
  </el-row>
</template>

<script>
import { getToken } from "@/utils/auth";
export default {
  data() {
    return {
      data: null,
      activeName: "second",
      loading: false
    };
  },
  methods: {
    getInfo() {
      this.loading = false;
      this.data = Web3Helper.getUserInfo(getToken());
      this.loading = true;
    },
    renewal(id) {
      this.$prompt('请输入续费金额', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputPattern: /\d/,
          inputErrorMessage: '格式不正确'
        }).then(({ value }) => {
          console.log(id, value);
          Web3Helper.renewAD(id, value)
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入'
          });       
        });
    },
    logOut() {
      this.$store.dispatch("LogOut");
      location.reload();
    },
    handleClick(tab, event) {
      console.log(tab, event);
    },
    goDetail(udfs, id, address, price) {
      this.$router.push({ path: "/article", query: { id: id } });
    }
  },
  mounted() {
    this.getInfo();
  }
};
</script>

<style lang="scss" scoped>
.el-row {
  margin-bottom: 20px;
  &:last-child {
    margin-bottom: 0;
  }
}

.el-col {
  border-radius: 4px;
}

.bg-purple-dark {
  background: #99a9bf;
}

.bg-purple {
  background: #fff;
}

.bg-purple-light {
  background: #e5e9f2;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}

.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}
.item {
  overflow: hidden;
  padding: 0 0 18px 0;
  border-bottom: 1px solid #eee;
  border-top: 1px solid #eee;
  .price {
    display: inline-block;
  }
  .more {
    display: inline-block;
    cursor: pointer;
    margin-left: 18px;
    float: right;
  }
  .abc {
    margin-left: 10px;
    display: inline-block;
    font-weight: normal;
    font-size: 12px;
    padding: 2px;
    border: 1px solid #444;
    border-radius: 4px;
  }
}
.list-home {
  .list-header {
    position: relative;
    h3 {
      display: inline-block;
    }
  }
  .mc {
    padding: 10px;
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
  }
  .info {
    right: 0px;
  }
  .publish {
    right: 90px;
  }
}
</style>
