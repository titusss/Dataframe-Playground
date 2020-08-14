<template>
  <div>
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group
        id="group-name"
        label="Name:"
        label-for="input-1"
      >
        <b-form-input
          id="input-name"
          v-model="form.name"
          required
          placeholder="Enter title"
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="group-url"
        label="API address:"
        label-for="input-2"
        description="Add the URL to the REST  API of the plugin's server."
      >
        <b-form-input
          id="input-url"
          v-model="form.url"
          type="url"
          required
          placeholder="https://..."
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="group-url"
        label="Description:"
        label-for="input-2"
      >
        <b-form-input
          id="input-url"
          v-model="form.desc"
          type="text"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="group-icon"
      >
        <b-form-file
          id="input-icon" role="form" enctype="multipart/form-data"
          v-model="form.icon"
          :state="Boolean(form.icon)"
          placeholder="Upload an icon for the tool..."
          drop-placeholder="Drop file here..."
          accept=".svg, .png, .jpg, .jpeg, .gif"
        ></b-form-file>
      </b-form-group>
      <b-button type="submit" variant="primary" @click="onSubmit">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  props: {
    backend_url: String,
  },
  data() {
    return {
      form: {
        url: '',
        name: '',
        desc: '',
        icon: null,
        db_entry_id: ''
      },
      show: true
    }
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault()
      const payload = this.form.icon;
      this.add_plugin(`${this.backend_url}/plugins`, payload);
    },
    onReset(evt) {
      evt.preventDefault()
      // Reset our form values
      this.form.url = ''
      this.form.name = ''
      this.form.icon = null
      // Trick to reset/clear native browser form validation state
      this.show = false
      this.$nextTick(() => {
        this.show = true
      })
    },
    add_plugin(path, payload) {
      if (this.$route.query.config) {
        this.form.db_entry_id = this.$route.query.config;
      }
      var data = new FormData();
        data.append('file', payload);
        data.append('form', JSON.stringify(this.form));
      let self = this;
      axios
        .post(path, data)
        .then(res => {
          this.$nextTick(() => {
            console.log("add_plugin res", res)
            self.$emit('plugins_change', res);
        });
      })
      .catch(error => {
        console.log(error);
      });
    },
  }
}
</script>



