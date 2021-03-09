

void get_GlobalRegional_2Dmatching_plots( TString fname="TrkSelectorComparison.root",string track_collection="hltIterL3MuonPixelTracks",
                                            double lowerCut=-1e9,double upperCut=1e9 , 
                                        int cutindex=0, string pic_name_sufix ="",string folder_name="ptemp/",int mode=1)
{
    string prefix;
    TFile fin(fname,"READ");
    cout<<"opening file"<<fname<<"\n";
    if (fin.IsZombie()) 
        return
    fin.cd();
    
    vector<double> minvals;
    vector<double> maxvals;
    vector<int> nbins;
    vector<string> branches;
    cout<<"setting up parms for hist and tree\n";
    branches.push_back("pt_track");minvals.push_back(0.0);maxvals.push_back(50.0);nbins.push_back(100);
    branches.push_back("qpt");minvals.push_back(-1.5);maxvals.push_back(1.5);nbins.push_back(100);
    branches.push_back("eta");minvals.push_back(-4);maxvals.push_back(4.0);nbins.push_back(40);
    branches.push_back("phi");minvals.push_back(-3.5);maxvals.push_back(3.5);nbins.push_back(35);
    branches.push_back("dz");minvals.push_back(-15);maxvals.push_back(15.0);nbins.push_back(100);
    branches.push_back("dxy");minvals.push_back(-0.4);maxvals.push_back(0.4);nbins.push_back(80);
    branches.push_back("ndelleta");minvals.push_back(-4.);maxvals.push_back(4.);nbins.push_back(80);
    branches.push_back("ndellphi");minvals.push_back(-4.);maxvals.push_back(4.);nbins.push_back(80);
    
    cout<<"obtaining the trees\n";
    string treeName =track_collection+"/tracks_RegReco";
    auto RegReco_tree=(TTree*) fin.Get(treeName.c_str());

    treeName =track_collection+"/tracks_RvR";
    auto RvR_tree=(TTree*) fin.Get(treeName.c_str());
    treeName =track_collection+"/tracks_missRvR";
    auto RvR_missing_tree=(TTree*) fin.Get(treeName.c_str());

    treeName =track_collection+"/tracks_GvR";
    auto GvR_tree=(TTree*) fin.Get(treeName.c_str());
    treeName =track_collection+"/tracks_RegReco_missingInGvR";
    auto RegReco_missing_tree=(TTree*) fin.Get(treeName.c_str());
    treeName =track_collection+"/tracks_GvR_matchedToRegReco";
    auto GvR_matched_tree=(TTree*)  fin.Get(treeName.c_str());
    treeName =track_collection+"/tracks_GvR_gained";
    auto GvR_gained_tree=(TTree*)  fin.Get(treeName.c_str());
    
    vector<TTree*> treelist;
    vector<string> prefix_string;
    vector<int> cmap;

    // Fname Setup 
    string    pic_name_prefix= "Match_";
 if(mode==1)
   {   
    treelist.push_back(RegReco_tree);prefix_string.push_back("RegReco_");cmap.push_back(kBlue);
//    treelist.push_back(RvR_tree);prefix_string.push_back("RvR_");cmap.push_back(kGreen);
//    treelist.push_back(RvR_missing_tree);prefix_string.push_back("RegReo_MissingIn_RvR_Tracks_");cmap.push_back(kRed);
    treelist.push_back(GvR_tree);prefix_string.push_back("GvR_Tracks_");cmap.push_back(kCyan);
    treelist.push_back(RegReco_missing_tree);prefix_string.push_back( "RegReco_MissedInGvR_Tracks_");cmap.push_back(kRed);
    treelist.push_back(GvR_matched_tree);prefix_string.push_back("GvR_Matched_Tracks_");cmap.push_back(kGreen);
    treelist.push_back(GvR_gained_tree);prefix_string.push_back("Addtional_GvR_Tracks_");cmap.push_back(kMagenta);
   } 
 if(mode==2)
   {   
    treelist.push_back(RegReco_tree);prefix_string.push_back("RegReco_");cmap.push_back(kBlue);
    treelist.push_back(RvR_tree);prefix_string.push_back("RvR_");cmap.push_back(kGreen);
    treelist.push_back(RvR_missing_tree);prefix_string.push_back("RegReo_MissingIn_RvR_Tracks_");cmap.push_back(kRed);
//    treelist.push_back(GvR_tree);prefix_string.push_back("GvR_Tracks_");cmap.push_back(kCyan);
//    treelist.push_back(RegReco_missing_tree);prefix_string.push_back( "RegReco_MissedInGvR_Tracks_");cmap.push_back(kRed);
//    treelist.push_back(GvR_matched_tree);prefix_string.push_back("GvR_Matched_Tracks_");cmap.push_back(kGreen);
//    treelist.push_back(GvR_gained_tree);prefix_string.push_back("Addtional_GvR_Tracks_");cmap.push_back(kMagenta);
   }
   if(mode == 3 )
    {
    	treelist.push_back(RegReco_tree);prefix_string.push_back("RegReco_");cmap.push_back(kBlue);
    	treelist.push_back(RvR_tree);prefix_string.push_back("RvR_");cmap.push_back(kRed);
	//treelist.push_back(RvR_missing_tree);prefix_string.push_back("RegReo_MissingIn_RvR_Tracks_");cmap.push_back(kRed);
    	treelist.push_back(GvR_tree);prefix_string.push_back("GvR_Tracks_");cmap.push_back(kMagenta);
    	//treelist.push_back(RegReco_missing_tree);prefix_string.push_back( "RegReco_MissedInGvR_Tracks_");cmap.push_back(kRed);
   	//treelist.push_back(GvR_matched_tree);prefix_string.push_back("GvR_Matched_Tracks_");cmap.push_back(kGreen+4);
   	//treelist.push_back(GvR_gained_tree);prefix_string.push_back("Addtional_GvR_Tracks_");cmap.push_back(kMagenta);
    }
 
   if(mode == 4 )
    {
    	//treelist.push_back(RegReco_tree);prefix_string.push_back("RegReco_");cmap.push_back(kBlue);
    	//treelist.push_back(RvR_tree);prefix_string.push_back("RvR_");cmap.push_back(kRed);
	treelist.push_back(RvR_missing_tree);prefix_string.push_back("RegReo_MissingIn_RvR_Tracks_");cmap.push_back(kBlue);
    	//treelist.push_back(GvR_tree);prefix_string.push_back("GvR_Tracks_");cmap.push_back(kMagenta);
    	treelist.push_back(RegReco_missing_tree);prefix_string.push_back( "RegReco_MissedInGvR_Tracks_");cmap.push_back(kRed);
   	//treelist.push_back(GvR_matched_tree);prefix_string.push_back("GvR_Matched_Tracks_");cmap.push_back(kGreen+4);
   	//treelist.push_back(GvR_gained_tree);prefix_string.push_back("Addtional_GvR_Tracks_");cmap.push_back(kMagenta);
    }


    cout<<"setting up branch addrs\n";
    double fvar[20],fvarA[2000],fvarB[2000];
    for (int i=0;i<8;i++)
    {
        if(i==cutindex)
        {
            if(lowerCut!=-1e9) minvals[i]=lowerCut;
            if(upperCut!=1e9)  maxvals[i] =upperCut;
        }
        if (i==6 )
        {
        
            for(int ii=0;ii<treelist.size();ii++)
                treelist[ii]->SetBranchAddress(branches[i].c_str(),fvarA);
            continue;
        }
        if (i==7 )
        {
           for(int ii=0;ii<treelist.size();ii++)
                treelist[ii]->SetBranchAddress(branches[i].c_str(),fvarB);
            continue;
        }
        
        for(int ii=0;ii<treelist.size();ii++)
                treelist[ii]->SetBranchAddress(branches[i].c_str(),&fvar[i]);
    }
    

    int ivar[20];
    
     for(int ii=0;ii<treelist.size();ii++)
    {
                treelist[ii]->SetBranchAddress("nRegions",&ivar[0]);
//                treelist[ii]->SetBranchAddress("event_id",&ivar[1]);
    }
    

    cout<<"setting up canvas\n";
    TCanvas *acanvas = new TCanvas("acanvas","acanvas",800,800);
    acanvas->cd();
    
    long int item_count;
    TH1D* aHistogram;
    vector<TH1D*> histlist;
    TTree * atree;
    TPaveStats *stats;
    string tmpstring;
    
    double statsY=0.9,statsDY=0.1;
    double min=3e9,bmin=3e9;
    
       TH2D* twoDEtaPhi=new TH2D("2detaphi","plot",100,-0.4,0.4,100,-0.4,0.4);
     	twoDEtaPhi->SetXTitle("#Delta#eta");
    	twoDEtaPhi->SetYTitle("#Delta#phi");
    
    for(int i=0;i<treelist.size();i++)
    {
        //***************************  RegReco missed in Gvr ****************************//
        
        atree=treelist[i];
        prefix=prefix_string[i];
        
        tmpstring=prefix+"_2DEtaPhi";
        twoDEtaPhi->SetTitle(tmpstring.c_str());
        twoDEtaPhi->Reset();
        item_count=atree->GetEntries();
        
        for(long int j=0;j<item_count;j++)
        {
            atree->GetEntry(j);
            
            if(fvar[0]<lowerCut or fvar[0]>upperCut) continue;
            min=3e9;
            for(int k=0;k<ivar[0];k++)
            {
                if(std::abs(fvarA[k])<std::abs(min))
                    min=fvarA[k];
            }
            
            bmin=3e9;
            for(int k=0;k<ivar[0];k++)
            {
                if(std::abs(fvarB[k])<std::abs(bmin))
                    bmin=fvarB[k];
            }
            twoDEtaPhi->Fill(min,bmin);
        }
        acanvas->cd();
        twoDEtaPhi->DrawClone("colz");
        tmpstring=folder_name+"2D_etaPhi_"+prefix+pic_name_sufix+".png";
        acanvas->SaveAs(tmpstring.c_str());
        cout<<"integral : "<<twoDEtaPhi->Integral()<<"\n";
    }
 
       TH2D* twoDdXYdZ=new TH2D("2dDxyDz","plot",100,-0.35,0.35,100,-28.0,28.0);
    	twoDdXYdZ->SetXTitle("dXY");
    	twoDdXYdZ->SetYTitle("dZ");
    for(int i=0;i<treelist.size();i++)
    {
        //***************************  RegReco missed in Gvr ****************************//
        
        atree=treelist[i];
        prefix=prefix_string[i];
        
        tmpstring=prefix+"_2D_Dxy_Dz";
        twoDdXYdZ->SetTitle(tmpstring.c_str());
        twoDdXYdZ->Reset();
        item_count=atree->GetEntries();
        
        for(long int j=0;j<item_count;j++)
        {
            atree->GetEntry(j);
            if(fvar[0]<lowerCut or fvar[0]>upperCut) continue;
         
	    twoDdXYdZ->Fill(fvar[5],fvar[4]);
        }
        acanvas->cd();
        twoDdXYdZ->DrawClone("colz");
        tmpstring=folder_name+"2D_DxyDz_"+prefix+pic_name_sufix+".png";
    
	acanvas->SaveAs(tmpstring.c_str());
        cout<<"integral : "<<twoDdXYdZ->Integral()<<"\n";
    }
 

   
    delete acanvas; 
}


void get_GlobalRegional_matching_plots( TString fname="TrkSelectorComparison.root",string track_collection="hltIterL3MuonPixelTracks",
                                        double lowerCut=-1e9,double upperCut=1e9 , 
                                        int cutindex=0, string pic_name_sufix ="",string folder_name="ptemp/",int mode=1)
{
    gStyle->SetStatStyle(0);
    gStyle->SetTitleStyle(0);
    gROOT->ForceStyle();
    
    gStyle->SetOptStat(1111);
    
    string prefix;
    TFile fin(fname,"READ");
    cout<<"opening file\n";
    if (fin.IsZombie()) 
        return
    fin.cd();
    
    vector<double> minvals;
    vector<double> maxvals;
    vector<int> nbins;
    vector<string> branches,labels;
    
        
    cout<<"setting up parms for hist and tree\n";
    branches.push_back("pt_track");minvals.push_back(0.0);maxvals.push_back(120.0);nbins.push_back(200);labels.push_back("pT_{reco} (GeV)");
    branches.push_back("qpt");minvals.push_back(-0.3);maxvals.push_back(0.3);nbins.push_back(100);labels.push_back("q/pT_{reco} ");
    branches.push_back("eta");minvals.push_back(-4);maxvals.push_back(4.0);nbins.push_back(40);labels.push_back("#eta_{reco}");
    branches.push_back("phi");minvals.push_back(-3.5);maxvals.push_back(3.5);nbins.push_back(35);labels.push_back("#phi_{reco}");
    branches.push_back("dz");minvals.push_back(-15);maxvals.push_back(15.0);nbins.push_back(100);labels.push_back("dZ_{reco}");
    branches.push_back("dxy");minvals.push_back(-0.4);maxvals.push_back(0.4);nbins.push_back(80);labels.push_back("dXY_{reco}");
    branches.push_back("ndelleta");minvals.push_back(-0.5);maxvals.push_back(0.5);nbins.push_back(80);labels.push_back("#Delta#eta");
    branches.push_back("ndellphi");minvals.push_back(-0.5);maxvals.push_back(0.5);nbins.push_back(80);labels.push_back("#Delta#phi");
    
    cout<<"obtaining the trees\n";
    auto dir = (TDirectory * ) fin.Get(track_collection.c_str());
    string treeName =track_collection+"/tracks_RegReco";
    auto RegReco_tree=(TTree*) fin.Get(treeName.c_str());
    cout<<"treeName = "<<treeName;
    if(RegReco_tree) cout<<" RegReco_tree \n";
    else cout<<"\n";
    
    treeName =track_collection+"/tracks_RvR";
    auto RvR_tree=(TTree*) fin.Get(treeName.c_str());
    cout<<"treeName = "<<treeName;
    if(RvR_tree) cout<<" RvR_tree \n";
    else cout<<"\n";
    treeName =track_collection+"/tracks_missRvR";
    auto RvR_missing_tree=(TTree*) fin.Get(treeName.c_str());
    cout<<"treeName = "<<treeName;
    if(RvR_missing_tree) cout<<" RvR_missing_tree \n";
    else cout<<"\n";

    treeName =track_collection+"/tracks_GvR";
    auto GvR_tree=(TTree*) fin.Get(treeName.c_str());
    cout<<"treeName = "<<treeName;
    if(GvR_tree) cout<<" GvR_tree \n";
    else cout<<"\n";

    treeName =track_collection+"/tracks_RegReco_missingInGvR";
    auto RegReco_missing_tree=(TTree*) fin.Get(treeName.c_str());
    cout<<"treeName = "<<treeName;
    if(RegReco_missing_tree) cout<<" RegReco_missing_tree \n";
    else cout<<"\n";
    
    treeName =track_collection+"/tracks_GvR_matchedToRegReco";
    auto GvR_matched_tree=(TTree*)  fin.Get(treeName.c_str());
    cout<<"treeName = "<<treeName;
    if(GvR_matched_tree) cout<<" GvR_matched_tree \n";
    else cout<<"\n";
    
    treeName =track_collection+"/tracks_GvR_gained";
    auto GvR_gained_tree=(TTree*)  fin.Get(treeName.c_str());
    cout<<"treeName = "<<treeName;
    if(GvR_gained_tree) cout<<" GvR_gained_tree \n";
    else cout<<"\n";
    
    
    vector<TTree*> treelist;
    vector<string> prefix_string;
    vector<int> cmap;

    // Fname Setup 
    string    pic_name_prefix= "Match_";
    
    if(mode == 1)
    {
    	treelist.push_back(RegReco_tree);prefix_string.push_back("RegReco_");cmap.push_back(kBlue);
//    treelist.push_back(RvR_tree);prefix_string.push_back("RvR_");cmap.push_back(kGreen);
//    treelist.push_back(RvR_missing_tree);prefix_string.push_back("RegReo_MissingIn_RvR_Tracks_");cmap.push_back(kRed);
    	treelist.push_back(GvR_tree);prefix_string.push_back("GvR_Tracks_");cmap.push_back(kCyan);
    	treelist.push_back(RegReco_missing_tree);prefix_string.push_back( "RegReco_MissedInGvR_Tracks_");cmap.push_back(kRed);
   	treelist.push_back(GvR_matched_tree);prefix_string.push_back("GvR_Matched_Tracks_");cmap.push_back(kGreen);
   	treelist.push_back(GvR_gained_tree);prefix_string.push_back("Addtional_GvR_Tracks_");cmap.push_back(kMagenta);
    }
   
   if(mode == 2)
    {
    	treelist.push_back(RegReco_tree);prefix_string.push_back("RegReco_");cmap.push_back(kBlue);
    	treelist.push_back(RvR_tree);prefix_string.push_back("RvR_");cmap.push_back(kGreen);
	treelist.push_back(RvR_missing_tree);prefix_string.push_back("RegReo_MissingIn_RvR_Tracks_");cmap.push_back(kRed);
    	//treelist.push_back(GvR_tree);prefix_string.push_back("GvR_Tracks_");cmap.push_back(kCyan);
    	//treelist.push_back(RegReco_missing_tree);prefix_string.push_back( "RegReco_MissedInGvR_Tracks_");cmap.push_back(kRed);
   	//treelist.push_back(GvR_matched_tree);prefix_string.push_back("GvR_Matched_Tracks_");cmap.push_back(kGreen);
   	//treelist.push_back(GvR_gained_tree);prefix_string.push_back("Addtional_GvR_Tracks_");cmap.push_back(kMagenta);
    }
 
   if(mode == 3 )
    {
    	treelist.push_back(RegReco_tree);prefix_string.push_back("RegReco_");cmap.push_back(kBlue);
    	treelist.push_back(RvR_tree);prefix_string.push_back("RvR_");cmap.push_back(kRed);
	//treelist.push_back(RvR_missing_tree);prefix_string.push_back("RegReo_MissingIn_RvR_Tracks_");cmap.push_back(kRed);
    	treelist.push_back(GvR_tree);prefix_string.push_back("GvR_Tracks_");cmap.push_back(kMagenta);
    	//treelist.push_back(RegReco_missing_tree);prefix_string.push_back( "RegReco_MissedInGvR_Tracks_");cmap.push_back(kRed);
   	//treelist.push_back(GvR_matched_tree);prefix_string.push_back("GvR_Matched_Tracks_");cmap.push_back(kGreen+4);
   	//treelist.push_back(GvR_gained_tree);prefix_string.push_back("Addtional_GvR_Tracks_");cmap.push_back(kMagenta);
    }
    if(mode == 4 )
    {
    	//treelist.push_back(RegReco_tree);prefix_string.push_back("RegReco_");cmap.push_back(kBlue);
    	//treelist.push_back(RvR_tree);prefix_string.push_back("RvR_");cmap.push_back(kRed);
	treelist.push_back(RvR_missing_tree);prefix_string.push_back("RegReo_MissingIn_RvR_Tracks_");cmap.push_back(kBlue);
    	//treelist.push_back(GvR_tree);prefix_string.push_back("GvR_Tracks_");cmap.push_back(kMagenta);
    	treelist.push_back(RegReco_missing_tree);prefix_string.push_back( "RegReco_MissedInGvR_Tracks_");cmap.push_back(kRed);
   	//treelist.push_back(GvR_matched_tree);prefix_string.push_back("GvR_Matched_Tracks_");cmap.push_back(kGreen+4);
   	//treelist.push_back(GvR_gained_tree);prefix_string.push_back("Addtional_GvR_Tracks_");cmap.push_back(kMagenta);
    }
   
    auto ntrees=treelist.size();
    
    cout<<"setting up branch addrs\n";
    double fvar[20],fvarA[200],fvarB[200];
    for (int i=0;i<8;i++)
    {
       
        if(i==cutindex)
        {
            if(lowerCut!=-1e9) minvals[i]=lowerCut;
            if(upperCut!=1e9)  maxvals[i] =upperCut;
        }
        if (i==6 )
        {
        
            for(int ii=0;ii<treelist.size();ii++)
            {
//             cout<<"i = "<<i<<" , ii = "<<ii<<"  : "<<branches[i].c_str()<<"\n";
             treelist[ii]->SetBranchAddress(branches[i].c_str(),fvarA);
            }
            
            continue;
        }
        if (i==7 )
        {
           for(int ii=0;ii<treelist.size();ii++)  
           {
//             cout<<"i = "<<i<<" , ii = "<<ii<<"  : "<<branches[i].c_str()<<"\n";
                treelist[ii]->SetBranchAddress(branches[i].c_str(),fvarB);
            }
            continue;
        }
        
        for(int ii=0;ii<treelist.size();ii++) 
           {
//             cout<<"i = "<<i<<" , ii = "<<ii<<"  : "<<branches[i].c_str()<<"\n";
                treelist[ii]->SetBranchAddress(branches[i].c_str(),&fvar[i]);
            }
    }
    
    int ivar[20];
    
     for(int ii=0;ii<treelist.size();ii++)
    {
                treelist[ii]->SetBranchAddress("nRegions",&ivar[0]);
//                treelist[ii]->SetBranchAddress("event_id",&ivar[1]);
    }

    cout<<"setting up canvas\n";
    TCanvas *acanvas = new TCanvas("acanvas","acanvas",800,800);
    acanvas->cd();
   
    long int item_count;
    TH1D* aHistogram;
    vector<TH1D*> histlist;
    TTree * atree;
    TPaveStats *stats;
    string tmpstring;
    
    double statsY=0.9,statsDY=0.1;
    
    cout<<" cut set for branch "<<branches[cutindex]<<"  : "<<lowerCut<<" , "<<upperCut<<"\n";
    for(int i=0;i<8;i++)
    {
//        histlist.clear();
        statsY=0.9;
//        acanvas->Clear();
        TLegend *leg=new TLegend(0.45,0.75,0.75,0.90);
        
        for(int ii=0;ii<treelist.size();ii++)
        {
            atree=treelist[ii];
            prefix=prefix_string[ii];
            auto col=cmap[ii];

            tmpstring=prefix+branches[i];
//            cout<<" Doing  "<<tmpstring<<"\n";
            aHistogram= new TH1D(tmpstring.c_str(),labels[i].c_str(),nbins[i],minvals[i],maxvals[i]);
            item_count=atree->GetEntries();
            for(long int j=0;j<item_count;j++)
            {
                atree->GetEntry(j);
                
                if(fvar[cutindex]<lowerCut or fvar[cutindex]>upperCut) continue;
                
                if(i==6)
                    {
                        double min=3e9;
                        for(int k=0;k<ivar[0];k++)
                        {
                            if(std::abs(fvarA[k])<std::abs(min))
                                min=fvarA[k];
                        }
                        aHistogram->Fill(min);
                        continue;
                    }
                 if(i==7)
                    {   
                        double min=3e9;
                        for(int k=0;k<ivar[0];k++)
                        {
                            if(std::abs(fvarB[k])<std::abs(min))
                                min=fvarB[k];
                        }
                        aHistogram->Fill(min);
                        continue;
                    }
                    
                    aHistogram->Fill(fvar[i]);
            }
            
            acanvas->cd();
 	    aHistogram->SetLineWidth(2);
            aHistogram->SetLineColor(col);
            aHistogram->SetYTitle("count");  
            aHistogram->SetXTitle(labels[i].c_str());  
            if(ii==0)             aHistogram->DrawClone();
            else                  aHistogram->DrawClone("sames");
            acanvas->Modified(); acanvas->Update();
            stats =(TPaveStats*)acanvas->GetPrimitive("stats");
            stats->SetName(prefix.c_str());
            stats->SetX1NDC(0.65);
            stats->SetX2NDC(0.90);
            stats->SetY1NDC(statsY);statsY-=statsDY;
            stats->SetY2NDC(statsY);
            acanvas->Update();         
            leg->AddEntry(aHistogram,prefix.c_str(),"l");
            histlist.push_back(aHistogram);
            
        }
        
        leg->SetEntrySeparation(0.1);
        acanvas->cd();
 //       leg->Draw();
   TPaveText *pt = new TPaveText(40,250,80,270);
   pt->AddText("Z#mu#mu (no PU)");
   pt->Draw();
        tmpstring=pic_name_prefix+branches[i]+pic_name_sufix;
        tmpstring+=".png";
        tmpstring=folder_name+tmpstring;
        acanvas->SaveAs(tmpstring.c_str());
        acanvas->Clear();
        histlist.push_back(aHistogram);
        //delete aHistogram;
    }
    
    delete acanvas;
    
    fin.Close();
}



void validate_trackcollection(string fname="TrkSelectorComparison.root",string track_collection="tracks")
{
    string output_folder=track_collection+"_validation";
    string tempstr="mkdir -p "+output_folder;
    gSystem->Exec(tempstr.c_str());

    string current_folder=output_folder+"/GlobalViaRegion";
    tempstr = "mkdir "+current_folder;
    gSystem->Exec(tempstr.c_str());

    string plot_folder=current_folder+"/SelectionFromGlobal/";
    tempstr = "mkdir "+plot_folder;
    gSystem->Exec(tempstr.c_str());
    get_GlobalRegional_matching_plots(fname,track_collection,0.0,1e9,0,"_GvR_ptCut0toInf",plot_folder,1);
    get_GlobalRegional_2Dmatching_plots(fname,track_collection,0.0,1e9,0,"_GvR_ptCut0toInf",plot_folder,1);

    plot_folder=current_folder+"/SelectionFromGlobal_pt_l3/";
    tempstr = "mkdir "+plot_folder;
    gSystem->Exec(tempstr.c_str());
    get_GlobalRegional_matching_plots(fname,track_collection,0.0,3.0,0,"_GvR_ptCut0to3",plot_folder,1);
    get_GlobalRegional_2Dmatching_plots(fname,track_collection,0.0,3.0,0,"_GvR_ptCut0to3",plot_folder,1);

    plot_folder=current_folder+"/SelectionFromGlobal_pt_g3/";
    tempstr = "mkdir "+plot_folder;
    gSystem->Exec(tempstr.c_str());
    get_GlobalRegional_matching_plots(fname,track_collection,3.0,1e9,0,"_GvR_ptCut3toInf",plot_folder,1);
    get_GlobalRegional_2Dmatching_plots(fname,track_collection,3.0,1e9,0,"_GvR_ptCut3toInf",plot_folder,1);


    /***************************  closureTest_RegionalViaRegion  ***************************/

    current_folder=output_folder+"/closureTest_RegionalViaRegion";
    tempstr = "mkdir "+current_folder;
    gSystem->Exec(tempstr.c_str());


    plot_folder=current_folder+"/SelectionFromRegional/";
    tempstr = "mkdir "+plot_folder;
    gSystem->Exec(tempstr.c_str());
    get_GlobalRegional_matching_plots(fname,track_collection,0.0,1e9,0,"_RvR_ptCut0toInf",plot_folder,2);
    get_GlobalRegional_2Dmatching_plots(fname,track_collection,0.0,1e9,0,"_RvR_ptCut0toInf",plot_folder,2);

    plot_folder=current_folder+"/SelectionFromRegional_pt_l3/";
    tempstr = "mkdir "+plot_folder;
    gSystem->Exec(tempstr.c_str());
    get_GlobalRegional_matching_plots(fname,track_collection,0.0,3.0,0,"_RvR_ptCut0to3",plot_folder,2);
    get_GlobalRegional_2Dmatching_plots(fname,track_collection,0.0,3.0,0,"_RvR_ptCut0to3",plot_folder,2);

    plot_folder=current_folder+"/SelectionFromRegional_pt_g3/";
    tempstr = "mkdir "+plot_folder;
    gSystem->Exec(tempstr.c_str());
    get_GlobalRegional_matching_plots(fname,track_collection,3.0,1e9,0,"_RvR_ptCut3toInf",plot_folder,2);
    get_GlobalRegional_2Dmatching_plots(fname,track_collection,30.,1e9,0,"_RvR_ptCut3toInf",plot_folder,2);

    /***************************  RvR_and_GvR  ***************************/

    current_folder=output_folder+"/RvR_and_GvR";
    tempstr = "mkdir "+current_folder;
    gSystem->Exec(tempstr.c_str());

    plot_folder=current_folder+"/Selection/";
    tempstr = "mkdir "+plot_folder;
    gSystem->Exec(tempstr.c_str());
    get_GlobalRegional_matching_plots(fname,track_collection,0.0,1e9,0,"_GvRandRvR_ptCut0toInf",plot_folder,3);
    get_GlobalRegional_2Dmatching_plots(fname,track_collection,0.0,1e9,0,"_GvRandRvR_ptCut0toInf",plot_folder,3);

    plot_folder=current_folder+"/Selection_pt_l3/";
    tempstr = "mkdir "+plot_folder;
    gSystem->Exec(tempstr.c_str());
    get_GlobalRegional_matching_plots(fname,track_collection,0.0,3.0,0,"_GvRandRvR_ptCut0to3",plot_folder,3);
    get_GlobalRegional_2Dmatching_plots(fname,track_collection,0.0,3.0,0,"_GvRandRvR_ptCut0to3",plot_folder,3);

    plot_folder=current_folder+"/Selection_pt_g3/";
    tempstr = "mkdir "+plot_folder;
    gSystem->Exec(tempstr.c_str());
    get_GlobalRegional_matching_plots(fname,track_collection,3.0,1e9,0,"_GvRandRvR_ptCut3toInf",plot_folder,3);
    get_GlobalRegional_2Dmatching_plots(fname,track_collection,3.0,1e9,0,"_GvRandRvR_ptCut3toInf",plot_folder,3);


    /***************************  missedTracksFromRegReco  ***************************/

    current_folder=output_folder+"/RvR_and_GvR/missedTracksFromRegReco";
    tempstr = "mkdir "+current_folder;
    gSystem->Exec(tempstr.c_str());

    plot_folder=current_folder+"/Selection/";
    tempstr = "mkdir "+plot_folder;
    gSystem->Exec(tempstr.c_str());
    get_GlobalRegional_matching_plots(fname,track_collection,0.0,1e9,0,"_GvRandRvR_ptCut0toInf",plot_folder,4);
    get_GlobalRegional_2Dmatching_plots(fname,track_collection,0.0,1e9,0,"_GvRandRvR_ptCut0toInf",plot_folder,4);

    plot_folder=current_folder+"/Selection_pt_l3/";
    tempstr = "mkdir "+plot_folder;
    gSystem->Exec(tempstr.c_str());;
    get_GlobalRegional_matching_plots(fname,track_collection,0.0,3.0,0,"_GvRandRvR_ptCut0to3",plot_folder,4);
    get_GlobalRegional_2Dmatching_plots(fname,track_collection,0.0,3.0,0,"_GvRandRvR_ptCut0to3",plot_folder,4);

    plot_folder=current_folder+"/Selection_pt_g3/";
    tempstr = "mkdir "+plot_folder;
    gSystem->Exec(tempstr.c_str());
    get_GlobalRegional_matching_plots(fname,track_collection,3.0,1e9,0,"_GvRandRvR_ptCut3toInf",plot_folder,4);
    get_GlobalRegional_2Dmatching_plots(fname,track_collection,3.0,1e9,0,"_GvRandRvR_ptCut3toInf",plot_folder,4);

    return ;

}

void validate(string fname="TrkSelectorComparison.root")
{
    vector<string> trackList;
    
    trackList.push_back("hltIterL3MuonPixelTracks");
//    trackList.push_back("hltIterL3MuonPixelTracksOpenMu");
//    trackList.push_back("hltIterL3MuonPixelTracksNoVtx");
//    trackList.push_back("hltIterL3FromL1MuonPixelTracks");
//    trackList.push_back("hltIter1PixelTracks");
//    trackList.push_back("hltIterL3FromL1MuonPixelTracksOpenMu");
//    trackList.push_back("hltPixelTracksForSeedsJpsi");
//    trackList.push_back("hltIterL3FromL1MuonPixelTracksNoVtx");
//    trackList.push_back("hltPixelTracksFromQuadrupletsRegL1TauSeeded");
//    trackList.push_back("hltPixelTracksFromTripletsRegL1TauSeeded");
//    trackList.push_back("hltIter0HighPtTkMuPixelTracks");
//    trackList.push_back("hltFastPVPixelTracks");
//    trackList.push_back("hltFastPVPixelTracksRecover");
//    trackList.push_back("hltIter1PixelTracksForBTag");
//    trackList.push_back("hltPixelTracksL3MuonNoVtx");
//    trackList.push_back("hltPixelTracksForSeedsPsiPrime");
//    trackList.push_back("hltPixelTracksForSeedsJpsiDoubleTrk");
//    trackList.push_back("hltPixelTracksForSeedsTau3muNoL1Mass");
//    trackList.push_back("hltPixelTracksForSeedsNR");
//    trackList.push_back("hltPixelTracksFromQuadrupletsRegForTau");
//    trackList.push_back("hltPixelTracksForNoPU");
    
    for(size_t i=0;i<trackList.size();i++)
     validate_trackcollection(fname,trackList[i]);

}

