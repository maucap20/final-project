import React from 'react';
import {Route, Switch } from 'react-router-dom';
import RegistrationForm from './RegistrationForm';
//import BrowseOpportunities from './components/BrowseOpportunities';
//import OpportunityDetails from './components/OpportunityDetails';
//import OrganizationProfile from './components/OrganizationProfile';
import UserDashboard from './UserDashboard';
import LoginForm from './LoginForm';

function App() {
  return (
    <div>
      <Switch>
        <Route exact path="/">  <UserDashboard /> </Route>
        <Route path="/register">  <RegistrationForm /> </Route>
        <Route path="/login"> <LoginForm /> </Route>
        {/* <Route path="/browse" element={<BrowseOpportunities />} /> */}
        {/* <Route path="/opportunity/:id" element={<OpportunityDetails />} /> */}
        {/* <Route path="/organization/:id" element={<OrganizationProfile />} /> */}
      </Switch>
    </div >
      );
  }

      export default App;