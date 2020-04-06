<template>
    <div class="base_wrapper">
        <img src="../assets/grid.svg" alt="" class="background_grid">
        <div class="grid_note">
            <b-icon icon="plus-square-fill"></b-icon>
            <p>Click to add data</p>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'baseContainer',
    }
</script>

<style scoped>
.base_wrapper{
    position: relative;
    text-align: center;
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