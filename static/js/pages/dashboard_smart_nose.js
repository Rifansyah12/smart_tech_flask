const clientId = Math.random().toString(16).substr(2, 8);
const host = "wss://smartnose-uninus.cloud.shiftr.io:443";

const options = {
  keepalive: 30,
  clientId: clientId,
  username: "smartnose-uninus",
  password: "0DKItrqWCc9bbr5w",
  protocolId: "MQTT",
  protocolVersion: 4,
  clean: true,
  reconnectPeriod: 1000,
  connectTimeout: 30 * 1000,
};

console.log("Menghubungkan ke Broker");
const client = mqtt.connect(host, options);

client.on("connect", () => {
  console.log("Terhubung");
  document.getElementById("status").innerHTML = "Terhubung";
  document.getElementById("status").style.color = "blue";

  client.subscribe("smartnose-uninus/#", { qos: 1 });
});

client.on("message", function (topic, payload) {
  if (topic === "smartnose-uninus/12345678/ADC") {
    document.getElementById("ADC").innerHTML = payload;
  } else if (topic === "smartnose-uninus/12345678/bac") {
    document.getElementById("bac").innerHTML = payload;
  } else if (topic === "smartnose-uninus/12345678/kelembaban") {
    document.getElementById("kelembaban").innerHTML = payload;
  } else if (topic === "smartnose-uninus/12345678/servo") {
    let servo1 = $("servo").data("ionRangeSlider");

    servo1.update({
      from: payload.toString(),
    });
  } else if (topic === "smartnose-uninus/12345678/led") {
    if (payload == "nyala") {
      document.getElementById("label-lampu1-nyala").classList.add("active");
      document.getElementById("label-lampu1-nyala").classList.remove("active");
    } else {
      document.getElementById("label-lampu1-nyala").classList.remove("active");
      document.getElementById("label-lampu1-nyala").classList.add("active");
    }
  }
  if (topic.includes("smartnose-uninus/status/12345678")) {
    document.getElementById(topic).innerHTML = payload;

    if (payload.toString() === "offline") {
      document.getElementById(topic).style.color = "red";
    } else if (payload.toString() === "online") {
      document.getElementById(topic).style.color = "blue";
    }
  }
});

function publishServo() {
  data = document.getElementById("servo").value;
  client.publish("smartnose-uninus/12345678/servo", data, {
    qos: 1,
    return: true,
  });
}

function publishLampu(value) {
  if (document.getElementById("lampu1-nyala").checked) {
    data = "nyala";
  }
  if (document.getElementById("lampu1-mati").checked) {
    data = "mati";
  }
  client.publish("smartnose-uninus/12345678/led", data, {
    qos: 1,
    return: true,
  });
}
