<script>
.slider:after {
    position: absolute;
    content: "OFF";
    top: 6px;
    right: 5px;
    color: #fff;
    font-size: 0.9em;
  }
  
  /* "ON" Text */
  input:checked + .slider:after {
    content: "ON";
    left: 10px;
  }
  </script>
