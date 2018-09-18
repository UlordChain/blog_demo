<template>
  <div v-if="loading">
    <el-row :gutter="20">
      <el-col :span="4">
        <div class="grid-content"></div>
      </el-col>
      <el-col :span="16">
        <div class="grid-content list-home bg-purple">
          <div class="list-header">
            <h3>Ulord博客</h3>
            <router-link to="/info" class="mc info">个人中心</router-link>
            <router-link to="/publish" class="mc publish">发布</router-link>
            <router-link to="/" class="mc back">返回主页</router-link>
          </div>
          <div class="list-content" v-if="loading">
            <h3 class="content-title">
              {{data.msg.title || "暂无"}}
            </h3>
            <div class="content-wrap">
              {{data.msg.body}}
            </div>
          </div>
        </div>
      </el-col>
      <el-col :span="4">
        <div class="grid-content"></div>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import { getToken } from "@/utils/auth";
export default {
  data() {
    return {
      data: null,
      loading: false,
      token: getToken(),
      id: this.$route.query.id
    };
  },
  methods: {
    getDetail() {
      this.loading = false;
      this.data = Web3Helper.queryResourceDetail(this.token, this.id);
      this.loading = true;
    }
  },

  mounted() {
    this.getDetail();
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
  .back {
    right: 153px;
  }
  .content-wrap {
    min-height: 700px;
  }
  .item {
    padding: 0 0 18px 0;
    border-bottom: 1px solid #eee;
    border-top: 1px solid #eee;
    .price {
      display: inline-block;
    }
    .more {
      cursor: pointer;
      text-align: right;
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
}
</style>