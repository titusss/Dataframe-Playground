 <!-- Main form for adding data tables/matrices --> 
 
 <template>
  <b-container class="bv-example-row">
    <b-row>
      <b-col>
        <h2>Add Data</h2>
        <b-form @submit="onSubmit" @reset="onReset" v-if="show">
          <b-form-group id="input-group-4" label="Type:" label-for="checkboxes-4">
            <b-form-radio-group v-model="form.type" id="checkboxes-4" required>
              <b-form-radio name="table" value="RadioTable">Table</b-form-radio>
              <b-form-radio name="category" value="RadioCategory">Category</b-form-radio>
            </b-form-radio-group>
          </b-form-group>
          <b-form-group id="input-group-2" label="Title:" label-for="input-2">
            <b-form-input id="input-2" v-model="form.title" required placeholder></b-form-input>
          </b-form-group>
          <b-form-group id="input-group-6" label="Source:" label-for="source-card">
            <b-card no-body id="source-card">
              <b-tabs card>
                <b-tab title="Upload" active>
                  <b-form-group
                    id="input-group-4"
                    description="Upload a CSV, TSV, or Excel from your machine."
                  >
                    <b-form-file
                      v-model="form.source.file"
                      :state="Boolean(form.source.file)"
                      placeholder="Choose a file or drop it here..."
                      drop-placeholder="Drop file here..."
                      accept=".txt"
                    ></b-form-file>
                    <!-- <div class="mt-3">Selected file: {{ form.source.file ? form.source.file.name : '' }}</div> -->
                  </b-form-group>
                </b-tab>
                <b-tab title="Database">
                  <b-form-group
                    id="input-group-3"
                    description="Select a dataset from our global database."
                  >
                    <b-form-select id="input-3" v-model="form.source.database" :options="foods"></b-form-select>
                  </b-form-group>
                </b-tab>
                <b-tab title="URL">
                  <b-form-group id="input-group-1" description="Enter a valid URL to your dataset.">
                    <b-form-input id="input-1" v-model="form.source.url" type="url" placeholder></b-form-input>
                  </b-form-group>
                </b-tab>
                <b-tab title="Text">
                  <b-form-group id="input-group-1" description="Paste comma-seperated values here.">
                    <b-form-textarea
                      id="textarea"
                      v-model="form.source.text"
                      placeholder="Comma-seperated values..."
                      rows="9"
                      max-rows="10000"
                    ></b-form-textarea>
                  </b-form-group>
                </b-tab>
              </b-tabs>
            </b-card>
          </b-form-group>
          <b-alert v-model="showErrorAlert" variant="danger" dismissible>{{sourceErrMsg}}</b-alert>
          <pre class="mt-3 mb-0">{{ text }}</pre>
          <b-button type="submit" variant="primary">Add</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-form>
      </b-col>
      <b-col class="center">
        <h2>Matrix Preview</h2>
        <matrix
          @delete="delete_matrix"
          v-bind:matrices="matrices"
          v-bind:rect_width="15"
          v-bind:rect_height="15"
          v-bind:gap="20"
        />
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import matrix from "./matrix.vue";
import axios from "axios";

export default {
  name: "addDataForm",
  components: {
    matrix
  },
  data() {
    return {
      sourceErrMsg: "",
      showErrorAlert: false,
      matrices: [],
      form: {
        title: "",
        type: [],
        source: {
          file: null,
          database: null,
          url: null,
          text: null
        }
      },
      text: "",
      foods: [
        { text: "Select One", value: null },
        "Carrots",
        "Beans",
        "Tomatoes",
        "Corn"
      ],
      show: true
    };
  },
  created() {
    this.fetch_matrices();
  },
  methods: {
    fetch_matrices() {
      const path = "http://localhost:5000/matrix";
      axios
        .get(path)
        .then(res => {
          console.log(res.data.matrix);
          this.matrices = res.data.matrix;
          console.log(this.matrices);
          // this.get_active_matrices(this.matrices);
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    add_matrix(payload) {
      const path = "http://localhost:5000/matrix";
      console.log(payload);
      axios
        .post(path, payload)
        .then(() => {
          this.fetch_matrices();
        })
        .catch(error => {
          console.log(error);
          this.fetch_matrices();
        });
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.validateForm(this.form.source);
      // this.$refs.bv_modal_addData.hide();
      const payload = this.form;
      this.add_matrix(payload);
      this.$emit('close');
    },
    onReset(evt) {
      this.$emit('close');
      console.log("reset");
      evt.preventDefault();
      // this.$refs.bv_modal_addData.hide();
    },
    validateForm(obj) {
      var properties = 0;
      for (var key in obj) {
        if (obj[key] !== null && obj[key] !== "") {
          properties++;
        }
      }
      if (properties < 1) {
        this.sourceErrMsg = "Please enter a data-source.";
        this.showErrorAlert = true;
      } else if (properties > 1) {
        this.sourceErrMsg = "Please enter no more than one data-source.";
        this.showErrorAlert = true;
      } else {
        return this.form;
      }
    },
    delete_matrix(deleted_matrix_id) {
      const path = `http://localhost:5000/matrix/${deleted_matrix_id}`;
      axios
        .delete(path)
        .then(() => {
          this.fetch_matrices();
          this.message = "Matrix removed!";
          this.showMessage = true;
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
          this.fetch_matrices();
        });
    },

    // get_active_matrices(matrices) {
    //   // Unneeded currently, remove in production
    //   var i = 0;
    //   for(i=0;i<matrices.length;i++) {
    //     if (Object.prototype.hasOwnProperty.call(this.matrices[i], 'title')) {
    //       this.active_matrices.push(this.matrices[i]);
    //     }
    //   }
    //   console.log(this.active_matrices);
    // }
    //   onSubmit(evt) {
    //     evt.preventDefault();
    //   },
    //   onReset(evt) {
    //     evt.preventDefault();
    //     // Reset our form values
    //     this.form.email = "";
    //     this.form.name = "";
    //     this.form.food = null;
    //     this.form.type = [];
    //     // Trick to reset/clear native browser form validation state
    //     this.show = false;
    //     this.$nextTick(() => {
    //       this.show = true;
    //     });
    //   }
    // }
  }
};
</script>