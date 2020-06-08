<template>
  <div>
    <div class="toast-center">
      <b-toast id="lock-toast" title="Session saved!" static no-auto-hide>
        This URL is now locked and cannot be modified.
      </b-toast>
    </div>
    <b-button-toolbar>
      <b-button-group class="mr-1">
        <b-button :disabled="disabled_lock" title="Save file" :variant="button_lock" @click="lock_session">
          <b-icon :icon="icon_lock" aria-hidden="false"></b-icon>
        </b-button>
        <b-button title="Load file" variant="light">
          <b-icon icon="cloud-download" aria-hidden="true"></b-icon>
        </b-button>
        <b-button title="New document" variant="light" @click="new_session">
          <b-icon icon="file-earmark" aria-hidden="true"></b-icon>
        </b-button>
      </b-button-group>
    </b-button-toolbar>
  </div>
</template>

<script>
import axios from "axios";
export default {
  props: {
    locked: Boolean
  },
  data() {
    return {
      icon_lock: "unlock",
      button_lock: "light",
      disabled_lock: true,
   }
  },
  created() {
    if (this.locked == true) {
      this.disabled_lock = true;
      this.button_lock = "dark";
      this.icon_lock = "lock"
    }
    else if(this.locked == false) {
      this.disabled_lock = false
    }
  },
  methods: {
    new_session() {
      this.$router.push({ path: ''})
    },
    lock_session() {
      this.disabled_lock = true
      const path = "http://0.0.0.0:5000/locked";
      var payload = new FormData();
        payload.append('url', JSON.stringify(this.$route.query.config));
      axios
        .post(path, payload)
        .then(res => {
          console.log(res)
          this.button_lock = "dark"
          this.icon_lock = "lock"
          this.$bvToast.show('lock-toast');
        });
    }
  }
}
</script>

<style scoped>
svg {
    margin: 0;
}
.btn-group {
    margin: 0 2rem 0 auto !important;
}
.toast-center {
  position: absolute;
  width: 100vw;
  text-align: center;
}
.b-toast {
  position: relative;
  display: inline-block;
}
</style>