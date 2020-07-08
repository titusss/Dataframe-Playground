<template>
  <div>
    <b-progress
      :value="loading.bar.value"
      :variant="loading.bar.variant"
      :key="loading.bar.variant"
      height="6px"
    ></b-progress>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loading: {
        state: false,
        bar: {
          variant: "primary",
          value: 0,
          timer: null
        }
      }
    };
  },
  mounted() {
    console.log("###########");
    this.loading.bar.timer = setInterval(() => {
      this.loading.bar.value = this.loading.bar.value + 50;
    }, 1000);
  },
  beforeDestroy() {
    console.log(this.loading.bar.timer);
    clearInterval(this.loading.bar.timer);
    this.loading.bar.timer = null;
  }
};
</script>