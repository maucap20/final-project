import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import RegistrationForm from './components/RegistrationForm';
import BrowseOpportunities from './components/BrowseOpportunities';
import OpportunityDetails from './components/OpportunityDetails';
import OrganizationProfile from './components/OrganizationProfile';
import UserDashboard from './components/UserDashboard';

function App() {
  return (
    <Router>
      <div>
        <Switch>
          <Route path="/" exact component={UserDashboard} />
          <Route path="/register" component={RegistrationForm} />
          <Route path="/browse" component={BrowseOpportunities} />
          <Route path="/opportunity/:id" component={OpportunityDetails} />
          <Route path="/organization/:id" component={OrganizationProfile} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;