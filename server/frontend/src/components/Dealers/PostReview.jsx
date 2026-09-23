import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';

const PostReview = () => {
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState("");
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);
  
  const { id } = useParams();
  const dealer_url = `/djangoapp/dealer/${id}`;
  const review_url = `/djangoapp/add_review`;
  const carmodels_url = `/djangoapp/get_cars`;

  const postreview = async () => {
    const firstname = sessionStorage.getItem("firstname") || "";
    const lastname = sessionStorage.getItem("lastname") || "";
    let name = `${firstname} ${lastname}`.trim();
    
    if (!name || name.includes("null") || name === "") {
      name = sessionStorage.getItem("username") || "Guest";
    }
    
    if (!model || review.trim() === "" || date === "" || year === "") {
      alert("All details are mandatory");
      return;
    }
    
    const model_split = model.split(" ");
    const make_chosen = model_split[0];
    const model_chosen = model_split.slice(1).join(" ");
    
    const jsoninput = JSON.stringify({
      name,
      dealership: id,
      review,
      purchase: true,
      purchase_date: date,
      car_make: make_chosen,
      car_model: model_chosen,
      car_year: year,
    });
    
    console.log(jsoninput);
    
    const res = await fetch(review_url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: jsoninput,
    });
    
    const json = await res.json();
    if (json.status === 200) {
      window.location.href = `${window.location.origin}/dealer/${id}`;
    }
  };

  const get_dealer = async () => {
    const res = await fetch(dealer_url, { method: "GET" });
    const retobj = await res.json();
    if (retobj.status === 200) {
      // ✅ Single object — NOT an array!
      setDealer(retobj.dealer);
    }
  };

  const get_cars = async () => {
    const res = await fetch(carmodels_url, { method: "GET" });
    const retobj = await res.json();
    if (retobj.CarModels) {
      setCarmodels(Array.from(retobj.CarModels));
    }
  };

  useEffect(() => {
    get_dealer();
    get_cars();
  }, [id]);

  return (
    <div>
      <Header />
      <div style={{ margin: "5%" }}>
        <h1 style={{ color: "darkblue" }}>{dealer?.full_name || "Loading..."}</h1>
        
        <div className="input_field">
          <label>Your Review:</label>
          <textarea
            id="review"
            cols="50"
            rows="7"
            value={review}
            onChange={(e) => setReview(e.target.value)}
            placeholder="Write your review here..."
          ></textarea>
        </div>
        
        <div className="input_field">
          <label>Purchase Date:</label>
          <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
        </div>
        
        <div className="input_field">
          <label>Car Make & Model:</label>
          <select
            name="cars"
            id="cars"
            value={model}
            onChange={(e) => setModel(e.target.value)}
          >
            <option value="" disabled>Choose Car Make and Model</option>
            {carmodels.map((carmodel, idx) => (
              <option
                key={idx}
                value={`${carmodel.CarMake} ${carmodel.CarModel}`}
              >
                {carmodel.CarMake} {carmodel.CarModel}
              </option>
            ))}
          </select>
        </div>
        
        <div className="input_field">
          <label>Car Year:</label>
          <input
            type="number"
            value={year}
            onChange={(e) => setYear(e.target.value)}
            min="2015"
            max="2026"
            placeholder="e.g. 2023"
          />
        </div>
        
        <button className="postreview" onClick={postreview}>
          Post Review
        </button>
      </div>
    </div>
  );
};

export default PostReview;
