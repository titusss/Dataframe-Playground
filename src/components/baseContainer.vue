<template>
  <div class="base_wrapper">
    <div class="base_inner" @click="$emit('show')">
      <img src="../assets/grid.svg" alt class="background_grid" />
      <div class="grid_note">
        <b-icon icon="plus-square-fill"></b-icon>
        <p>Click to add data</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "baseContainer"
};
</script>

<style scoped>
.base_wrapper {
  position: relative;
  text-align: center;
}
.base_inner {
    display: inline-block;
    cursor: pointer;
}
.grid_note {
  position: absolute;
  top: 50%;
  text-align: center;
  left: 50%;
  transform: translate(-50%, -50%);
}
p {
  margin: 0;
}
</style>