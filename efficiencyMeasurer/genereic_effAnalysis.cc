/*

    Mesures and plots eff.  vs pT and eta
        Plots various other histograms too.

        Requires 2 barches in a tree :
            matchedGenP4      : 
            matchedRecoP4     :
            missedGenP4       :
    p4 stored as a std::vector<float> .. with exactly 4 entries  pt eta phi and M, to be used to get TLorentzVector as,
                    temp=genMatchedP4->at(j);
                    aTLorentzVector.SetPtEtaPhiM(temp[0],temp[1],temp[2],temp[3]);
	            
*/

void getPtEtaCutTotalHistograms(TTree *tree,
                                TString matchedGenP4,TString matchedRecoP4,TString missedGenP4,
                                TH1F *hist_allEta,TH1F *hist_matchedEta,
				                TH1F *hist_allPt,TH1F* hist_matchedPt,
				                TH1F * hist_matchedRecoPt,
				                TH1F *deltaPts, TH1F * deltaEtas ,TH1F * deltaRMatch,
				                float pTmin_,float dRmax=9999.9,bool resetHist=false)
{
    std::vector<std::vector<double>>  *genMatchedMuonP4(nullptr),*genMissMuonP4(nullptr);
    std::vector<std::vector<double>>  *genMatchedP4(nullptr),*genMissP4(nullptr);
    std::vector<std::vector<double>>  *genMatchedRecoMuonP4(nullptr),*genMatchedRecoP4(nullptr);
    std::vector<double> temp;

    TLorentzVector aTLorentzVector,bTLorentzVector;
 

    tree->SetBranchAddress(matchedRecoP4,&genMatchedRecoP4);
    tree->SetBranchAddress(matchedGenP4,&genMatchedP4);
    tree->SetBranchAddress(missedGenP4,&genMissP4);
    
    if(resetHist)
    {
            hist_allEta->Reset();
    	    hist_matchedEta->Reset();
	        hist_allPt->Reset();
	        hist_matchedPt->Reset();

    	    deltaPts->Reset();
    	    deltaEtas->Reset();
    }

   // std::cout<<"Doing "<<tree->GetEntries()<<"  events \n";
    for(int i=0;i<tree->GetEntries();i++)
    	{
	    	tree->GetEntry(i);
		    if(i%4096==0) std::cout<<"Doing event i = "<<i<<"\n";
		
        for(int j=0;j<genMatchedP4->size();j++)
		{
	            temp=genMatchedP4->at(j);
                    aTLorentzVector.SetPtEtaPhiM(temp[0],temp[1],temp[2],temp[3]);
	            temp=genMatchedRecoP4->at(j);
                    bTLorentzVector.SetPtEtaPhiM(temp[0],temp[1],temp[2],temp[3]);
		     		
	     	   if(aTLorentzVector.Perp() < pTmin_) continue;
	     	   
               auto dR = aTLorentzVector.DeltaR(bTLorentzVector) ;

               if( dR >dRmax)
               {
                    hist_allPt->Fill(aTLorentzVector.Perp());       		
		    	    hist_allEta->Fill(aTLorentzVector.Eta());
                    continue;
               }

                deltaRMatch->Fill(dR);
		        
		        hist_allPt->Fill(aTLorentzVector.Perp());       		
	     	    hist_matchedPt->Fill(aTLorentzVector.Perp());       		
	     	    hist_matchedRecoPt->Fill(bTLorentzVector.Perp());       		


		        hist_allEta->Fill(aTLorentzVector.Eta());
		        hist_matchedEta->Fill(bTLorentzVector.Eta());
		    
		    //std::cout<<"deltaPts  "<<abs(aTLorentzVector.Perp()-bTLorentzVector.Perp())<<"\n";
		    //std::cout<<"deltaEtas  "<<abs(aTLorentzVector.Eta()-bTLorentzVector.Eta())<<"\n";
		    deltaPts->Fill(abs(aTLorentzVector.Perp()-bTLorentzVector.Perp()));
		    deltaEtas->Fill(abs(aTLorentzVector.Eta()-bTLorentzVector.Eta()));

		}
		
		for(int j=0;j<genMissP4->size();j++)
		{
 		    temp=genMissP4->at(j);
                    aTLorentzVector.SetPtEtaPhiM(temp[0],temp[1],temp[2],temp[3]);
		    
		    if(aTLorentzVector.Perp() < pTmin_) continue;
	     	    hist_allPt->Fill(aTLorentzVector.Perp());       		
		    
		    hist_allEta->Fill(aTLorentzVector.Eta());
		}

	}

}



void doEfficiencyPlotsForASet(  std::vector<TString> fnames,string folder, string suffix,
                                TString tree_name,
                                TString bname_matchedGenP4, TString bname_matchedRecoP4, TString bname_missedGenP4,
                                float pTmin=1.0,float dRmax =9999.9 )
{
	
     	gStyle->SetOptStat("eoum");

        
        if(fnames.size()==0)
        {
            fnames.push_back("efficiencyFromAOD.root");
        }

	   TFile *file =new TFile(fnames[0]);;
       
       size_t ptBins =60;
       size_t etaBins=40;

	   TH1F * hist_allEta        = new TH1F("eta","GEN #eta",etaBins,-3.0,3.0);
	   TH1F * hist_matchedEta    = new TH1F("etaMatched","GEN #eta of Matched GenParticle",etaBins,-3.0,3.0);
	   TH1F * hist_allPt         = new TH1F("pT","GEN pT of GenParticle",ptBins,0.0,30);
	   TH1F * hist_matchedPt     = new TH1F("pTMatched","pT of Matched GenParticles",ptBins,0.0,30.0);
       TH1F * hist_matchedRecoPt = new TH1F("pTReco","RECO pT of Matched GenParticles",ptBins,0.0,30);

       auto *histDeltaRs   = new TH1F("DeltaR","#delta R ",20,0.0,0.2);
       auto *histDeltaPts  = new TH1F("DeltaPts","#delta pT",50,0.0,100.0);
       auto *histDeltaEtas = new TH1F("DeltaEta","#delta #eta",10,0.0,0.10);


    std::vector<TH1F*> histograms_to_plot; 
    vector<TString> xLabel,yLabel;
    vector<uint> lineColour,lineWidth;
    vector<bool> plotLog;

    
    histograms_to_plot.push_back(hist_allEta);   xLabel.push_back("#delta pT [GeV]");   yLabel.push_back("#");   
		lineColour.push_back(kBlue);   lineWidth.push_back(2);   plotLog.push_back(false);   

    histograms_to_plot.push_back(hist_allPt);   xLabel.push_back("pT [GeV]");   yLabel.push_back("#");   
		lineColour.push_back(kBlue);   lineWidth.push_back(2);   plotLog.push_back(false);   

    histograms_to_plot.push_back(hist_matchedPt);   xLabel.push_back(" pT [GeV]");   yLabel.push_back("#");   
		lineColour.push_back(kBlue);   lineWidth.push_back(2);   plotLog.push_back(false);   

    histograms_to_plot.push_back(hist_matchedRecoPt);   xLabel.push_back(" pT [GeV]");   yLabel.push_back("#");   
		lineColour.push_back(kBlue);   lineWidth.push_back(2);   plotLog.push_back(false);   

    histograms_to_plot.push_back(hist_matchedEta);   xLabel.push_back("#eta");   yLabel.push_back("#");   
		lineColour.push_back(kBlue);   lineWidth.push_back(2);   plotLog.push_back(false);   

    histograms_to_plot.push_back(histDeltaRs);   xLabel.push_back("#Delta R ");   yLabel.push_back("#");   
		lineColour.push_back(kBlue);   lineWidth.push_back(2);   plotLog.push_back(false);   

    histograms_to_plot.push_back(histDeltaPts);   xLabel.push_back("#delta pT [GeV]");   yLabel.push_back("#");   
		lineColour.push_back(kBlue);   lineWidth.push_back(2);   plotLog.push_back(false);   

    histograms_to_plot.push_back(histDeltaEtas);   xLabel.push_back("#delta #Eta");   yLabel.push_back("#");   
		lineColour.push_back(kBlue);   lineWidth.push_back(2);   plotLog.push_back(false);   
    
     
    //file->Close();
     for(int i=0;i<fnames.size();i++)
     {
        
        std::cout<<i<<" / "<<fnames.size()<<" : Doing " <<fnames[i]<<"\n";
	    file= new TFile(fnames[i]);
        if(file->IsZombie()) continue;

        TTree * tree = (TTree *) file->Get(tree_name);
	    auto doReset = false;
	    
        if(i==0) doReset =true;
        
        /*
        void getPtEtaCutTotalHistograms(TTree *tree,
                                TString matchedGenP4,TString matchedRecoP4,TString missedGenP4,
                                TH1F *hist_allEta,TH1F *hist_matchedEta,
				                TH1F *hist_allPt,TH1F* hist_matchedPt,
				                TH1F * hist_matchedRecoPt,
				                TH1F *deltaPts,TH1F * deltaRMatch,
				                float pTmin_,float dRmax=9999.9,bool resetHist=false) */
 
 	    getPtEtaCutTotalHistograms(tree,bname_matchedGenP4,bname_matchedRecoP4,bname_missedGenP4,
                                    hist_allEta, hist_matchedEta,hist_allPt, hist_matchedPt, hist_matchedRecoPt,
                                    histDeltaPts,histDeltaEtas, histDeltaRs,
	    			                pTmin,dRmax , doReset);
	    	
	    file->Close();
		  
        std::cout<<"       hist_allPt -> Integral () :  "<<hist_allPt->Integral()<<"\n";
        std::cout<<"       hist_matchedPt -> Integral () :  "<<hist_matchedPt->Integral()<<"\n";
        std::cout<<"       hist_allEta -> Integral () :  "<<hist_allEta->Integral()<<"\n";
        std::cout<<"       hist_matchedEta-> Integral () :  "<<hist_matchedEta->Integral()<<"\n";
    }
  	
  auto c1=new TCanvas("c1","mytitle");
  string img_save_type(".png"),picname,prefix(folder),save_fname;
  auto statsY=0.9    ;
  auto statsDY=0.15  ;
  TPaveStats *stats;
  TLegend *leg=new TLegend(0.12,0.75,0.35,0.85);

  TEfficiency *pEff= new TEfficiency();
  for(int i=0;i< histograms_to_plot.size();i++)
  {
  	auto ahist=histograms_to_plot.at(i);
	c1->Clear();
  	c1->SetTitle(ahist->GetTitle());
	if(plotLog[i])  gPad->SetLogy();
	else   gPad->SetLogy(0);
	ahist->SetXTitle(xLabel[i]);
	ahist->SetYTitle(yLabel[i]);
        ahist->SetLineColor(lineColour[i]);
        ahist->SetLineWidth(lineWidth[i]);
        ahist->Draw();
        
    std::cout<<"printing histogram  : "<<picname<<" I : "<<ahist->Integral()<<" :  T  : "<<ahist->GetTitle()<<"  : N   "<<ahist->GetName()<<"  :  "<<i<<"\n";
	picname=prefix+string(ahist->GetName())+ suffix +img_save_type;
	c1->SaveAs(picname.c_str());
  }
 

/////////////////////		 pT  gen vs reco comparison        	/////////////////////////
  c1->Clear()   ;
  statsY=0.9    ;
  statsDY=0.15  ;
  

  gPad->SetLogy();
  hist_matchedPt->SetLineWidth(2);
  hist_matchedPt->SetLineColor(kBlue);
  hist_matchedPt->SetName("GEN pT");
  hist_matchedPt->Draw();
  leg->AddEntry(hist_matchedPt,"GEN","l");
  c1->Modified(); c1->Update();
  
  stats =(TPaveStats*)c1->GetPrimitive("stats");
  stats->SetName("GEN pT");

  stats->SetX1NDC(0.7);
  stats->SetX2NDC(0.9);

  stats->SetY1NDC(statsY);statsY-=statsDY;
  stats->SetY2NDC(statsY);
  c1->Modified(); c1->Update();

  hist_matchedRecoPt->SetLineWidth(2);
  hist_matchedRecoPt->SetLineColor(kRed);
  hist_matchedRecoPt->SetName("RECO pT");
  hist_matchedRecoPt->Draw("SAMES");
  leg->AddEntry(hist_matchedRecoPt,"RECO","l");
  
  c1->Modified(); c1->Update();
  stats =(TPaveStats*)c1->GetPrimitive("stats");
  stats->SetName("RECO pT");
  stats->SetX1NDC(0.7);
  stats->SetX2NDC(0.9);

  stats->SetY1NDC(statsY);statsY-=statsDY;
  stats->SetY2NDC(statsY);
  c1->Modified(); c1->Update();

  leg->SetEntrySeparation(0.1);
  leg->Draw();
  
  c1->SetTitle("pT : GEN & RECO");
  c1->Modified();c1->Update();  
  save_fname="pT_genReco_Comparison";
  picname=prefix+save_fname+suffix+img_save_type;
  c1->SaveAs(picname.c_str());

  gPad->SetLogy(0);

///////////////////////////////////////////////////////////////////////////
  
  if(TEfficiency::CheckConsistency(*hist_matchedEta,*hist_allEta))
  {
  	delete pEff;
	pEff = new TEfficiency(*hist_matchedEta,*hist_allEta);
	pEff->SetTotalHistogram(*hist_allEta,"f");
  	pEff->SetPassedHistogram(*hist_matchedEta,"f");
  	pEff->SetName("#epsilon vs  #eta");
  	pEff->SetTitle("#epsilon vs  #eta;#eta;#epsilon");
  	pEff->Draw("AP");
  	
	gPad->Update(); 
    auto graph = pEff->GetPaintedGraph(); 
    graph->SetMinimum(0);graph->SetMaximum(1); 
    gPad->Update(); 

  	save_fname="EtaEfficiency";
  	picname=prefix+save_fname+suffix+img_save_type;
  	c1->SaveAs(picname.c_str());
  	c1->Clear();
  }
 	
  if(TEfficiency::CheckConsistency(*hist_matchedPt,*hist_allPt))
  {
  	delete pEff;
	pEff = new TEfficiency(*hist_matchedPt,*hist_allPt);
	pEff->SetTotalHistogram(*hist_allPt,"f");
  	pEff->SetPassedHistogram(*hist_matchedPt,"f");
  	pEff->SetName("#epsilon vs  pT");
  	pEff->SetTitle("#epsilon vs  pT;pT [GeV] ;#epsilon");
  	pEff->Draw("AP");
 
    gPad->Update(); 
    auto graph = pEff->GetPaintedGraph(); 
    graph->SetMinimum(0);graph->SetMaximum(1); 
    gPad->Update(); 

  	save_fname="PtEfficiency";
  	picname=prefix+save_fname+suffix+img_save_type;
  	c1->Modified();c1->Update();
	c1->SaveAs(picname.c_str());
  	c1->Clear();
  }

  c1->Close();
  delete c1;
  
delete hist_allEta       ;
delete hist_matchedEta   ;
delete hist_allPt        ;
delete hist_matchedPt    ;
delete hist_matchedRecoPt;

}



void doEfficiencyPlotsDoublePhoton()
{
    std::vector<TString> fnames;
    string folder("plots/"),suffix("");
    TString tree_name("eff");
    TString bname_matchedGenP4, bname_matchedRecoP4, bname_missedGenP4;
    float pTmin=1.0;

    tree_name="effMeasure/RecoEff";
    bname_matchedGenP4  =  "genMatchedGedPhotonP4";
    bname_matchedRecoP4 =  "genMatchedRecoGedPhotonP4";
    bname_missedGenP4   =  "genMissGedPhotonP4";
    folder = "plots/DoublePhotonFlatPt0To20/" ;
    suffix = "_ged" ;
    pTmin  = 1.0 ;
    fnames.push_back("DoublePhoton0To40FlatPtAODSIM_EffMesure.root");
    doEfficiencyPlotsForASet(fnames,folder,suffix,tree_name,
                              bname_matchedGenP4,bname_matchedRecoP4,bname_missedGenP4,
                              pTmin);
    fnames.clear();

    tree_name="effMeasure/RecoEff";
    bname_matchedGenP4  =  "genMatchedSuperClusterPhotonP4";
    bname_matchedRecoP4 =  "genMatchedRecoSuperClusterPhotonP4";
    bname_missedGenP4   =  "genMissSuperClusterPhotonP4";
    folder = "plots/DoublePhotonFlatPt0To20/" ;
    suffix = "_sc" ;
    pTmin  = 1.0 ;
    fnames.push_back("DoublePhoton0To40FlatPtAODSIM_EffMesure.root");
    doEfficiencyPlotsForASet(fnames,folder,suffix,tree_name,
                              bname_matchedGenP4,bname_matchedRecoP4,bname_missedGenP4,
                              pTmin);
    fnames.clear();

    tree_name="effMeasure/RecoEff";
    bname_matchedGenP4  =  "genMatchedPhotonP4";
    bname_matchedRecoP4 =  "genMatchedRecoPhotonP4";
    bname_missedGenP4   =  "genMissPhotonP4";
    folder = "plots/DoublePhotonFlatPt0To20/" ;
    suffix = "_pat" ;
    pTmin  = 1.0 ;
    fnames.push_back("DoublePhoton0To40FlatPtAODSIM_1_inMINIAODSIM_EffMeasure.root");
    doEfficiencyPlotsForASet(fnames,folder,suffix,tree_name,
                              bname_matchedGenP4,bname_matchedRecoP4,bname_missedGenP4,
                              pTmin);
    fnames.clear();




}

void doEfficiencyPlotsBS2MMGPrivateRun3()
{
    std::vector<TString> fnames;
    string folder("plots/"),suffix("");
    TString tree_name("eff");
    TString bname_matchedGenP4, bname_matchedRecoP4, bname_missedGenP4;
    float pTmin=1.0;

    tree_name="effMeasure/RecoEff";
    bname_matchedGenP4  =  "genMatchedGedPhotonP4";
    bname_matchedRecoP4 =  "genMatchedRecoGedPhotonP4";
    bname_missedGenP4   =  "genMissGedPhotonP4";
    folder = "plots/Bs2MMG_Run3/" ;
    suffix = "_ged" ;
    pTmin  = 1.0 ;
    fnames.push_back("efficiencyFromAOD_bsmmg2023.root");
    doEfficiencyPlotsForASet(fnames,folder,suffix,tree_name,
                              bname_matchedGenP4,bname_matchedRecoP4,bname_missedGenP4,
                              pTmin);
    fnames.clear();

    tree_name="effMeasure/RecoEff";
    bname_matchedGenP4  =  "genMatchedSuperClusterPhotonP4";
    bname_matchedRecoP4 =  "genMatchedRecoSuperClusterPhotonP4";
    bname_missedGenP4   =  "genMissSuperClusterPhotonP4";
    folder = "plots/Bs2MMG_Run3/" ;
    suffix = "_sc" ;
    pTmin  = 1.0 ;
    fnames.push_back("efficiencyFromAOD_bsmmg2023.root");
    doEfficiencyPlotsForASet(fnames,folder,suffix,tree_name,
                              bname_matchedGenP4,bname_matchedRecoP4,bname_missedGenP4,
                              pTmin);
    fnames.clear();

    //tree_name="effMeasure/RecoEff";
    //bname_matchedGenP4  =  "genMatchedPhotonP4";
    //bname_matchedRecoP4 =  "genMatchedRecoPhotonP4";
    //bname_missedGenP4   =  "genMissPhotonP4";
    //folder = "plots/Bs2MMG_Run3/" ;
    //suffix = "_pat" ;
    //pTmin  = 1.0 ;
    //fnames.push_back("DoublePhoton0To40FlatPtAODSIM_1_inMINIAODSIM_EffMeasure.root");
    //doEfficiencyPlotsForASet(fnames,folder,suffix,tree_name,
    //                          bname_matchedGenP4,bname_matchedRecoP4,bname_missedGenP4,
    //                          pTmin);
    //fnames.clear();




}

void doEfficiencyPlotsRelValTTXRun3MiniAODSIM()
{
    std::vector<TString> fnames;
    string folder("plots/"),suffix("");
    TString tree_name("eff");
    TString bname_matchedGenP4, bname_matchedRecoP4, bname_missedGenP4;
    float pTmin=1.0;
    
    tree_name="effMeasure/RecoEff";
    bname_matchedGenP4  =  "genMatchedPhotonP4";
    bname_matchedRecoP4 =  "genMatchedRecoPhotonP4";
    bname_missedGenP4   =  "genMissPhotonP4";
    folder = "plots/RelValTTX/" ;
    suffix = "_pat" ;
    pTmin  = 1.0 ;

    fnames.push_back("relvalFiles/store_relval_CMSSW_11_3_0_pre1_RelValTTbar_14TeV_MINIAODSIM_113X_mcRun3_2021_realistic_v1_8c2s10GB-v1_10000_15d6b536-2759-46a2-8919-0de13dcdd21b.root");
	fnames.push_back("relvalFiles/store_relval_CMSSW_11_3_0_pre1_RelValTTbar_14TeV_MINIAODSIM_113X_mcRun3_2021_realistic_v1-v1_10000_219a6e86-a80e-4612-9bda-65e236fe3a0b.root");
	fnames.push_back("relvalFiles/store_relval_CMSSW_11_3_0_pre1_RelValTTbar_14TeV_MINIAODSIM_113X_mcRun3_2021_realistic_v1_8c2s10GB-v2_10000_08a6802a-d564-4efa-a338-435aa873d100.root");
	fnames.push_back("relvalFiles/store_relval_CMSSW_11_3_0_pre1_RelValZpTT_1500_14_MINIAODSIM_113X_mcRun3_2021_realistic_v1-v1_10000_0db22842-ca2a-407c-95f3-5ad29ea25b39.root");
	fnames.push_back("relvalFiles/store_relval_CMSSW_11_3_0_pre1_RelValZTT_14_MINIAODSIM_113X_mcRun3_2021_realistic_v1-v1_10000_bbb6d93f-3afb-404a-bfce-1013c8ee633c.root");
	fnames.push_back("relvalFiles/store_relval_CMSSW_11_3_0_pre2_RelValTTbar_14TeV_MINIAODSIM_113X_mcRun3_2021_realistic_v2_rsb-v1_10000_d18dd252-4d70-4a58-9448-b309b49dc6f3.root");
	fnames.push_back("relvalFiles/store_relval_CMSSW_11_3_0_pre2_RelValZpTT_1500_14_MINIAODSIM_113X_mcRun3_2021_realistic_v2_rsb-v1_10000_f9818dae-d6f2-4d67-a258-b6f0e7ec1967.root");
	fnames.push_back("relvalFiles/store_relval_CMSSW_11_3_0_pre2_RelValZTT_14_MINIAODSIM_113X_mcRun3_2021_realistic_v2_rsb-v1_10000_0b797138-50c6-467f-9243-a5bba48a0e42.root");
	fnames.push_back("relvalFiles/store_relval_CMSSW_11_3_0_pre2_SCRAMV3_RelValTTbar_14TeV_MINIAODSIM_113X_mcRun3_2021_realistic_v2-v3_00000_c4ade6b1-0c2a-41c2-bef0-99dda3ac543d.root");
	fnames.push_back("relvalFiles/store_relval_CMSSW_11_3_0_pre2_SCRAMV3_RelValTTbar_14TeV_MINIAODSIM_113X_mcRun3_2021_realistic_v2-v4_00000_3f3a2a23-f722-4f02-8f5d-3f6905fc765c.root");
	fnames.push_back("relvalFiles/store_relval_CMSSW_11_3_0_pre3_RelValTTbar_14TeV_MINIAODSIM_113X_mcRun3_2021_realistic_v4-v1_00000_64a26a01-b0e7-41b3-82a4-b759df5af31c.root");
	fnames.push_back("relvalFiles/store_relval_CMSSW_11_3_0_pre3_RelValZpTT_1500_14_MINIAODSIM_113X_mcRun3_2021_realistic_v4-v1_00000_06517dee-8ec7-437b-b482-98e5371e8c2f.root");
	fnames.push_back("relvalFiles/store_relval_CMSSW_11_3_0_pre3_RelValZTT_14_MINIAODSIM_113X_mcRun3_2021_realistic_v4-v1_00000_d5ce0496-13c7-42fd-964b-6be64c858a24.root");
	fnames.push_back("relvalFiles/store_relval_CMSSW_11_3_0_pre4_RelValTTbar_14TeV_MINIAODSIM_113X_mcRun3_2021_realistic_v7-v1_00000_9c9a2f5d-7981-42d4-914a-b1113bbe2a9b.root");
	fnames.push_back("relvalFiles/store_relval_CMSSW_11_3_0_pre4_RelValZpTT_1500_14_MINIAODSIM_113X_mcRun3_2021_realistic_v7-v1_00000_aef50134-f3dd-45b3-a0d3-bf963e22f5e1.root");
	fnames.push_back("relvalFiles/store_relval_CMSSW_11_3_0_pre4_RelValZTT_14_MINIAODSIM_113X_mcRun3_2021_realistic_v7-v1_00000_ec6a35f6-3d1e-4840-ac32-cef776c01371.root");
	fnames.push_back("relvalFiles/store_relval_CMSSW_11_3_0_pre5_RelValTTbar_14TeV_MINIAODSIM_113X_mcRun3_2021_realistic_v7-v1_00000_33db2081-35d7-442c-801f-5fa3c51c5c28.root");
	fnames.push_back("relvalFiles/store_relval_CMSSW_11_3_0_pre5_RelValZpTT_1500_14_MINIAODSIM_113X_mcRun3_2021_realistic_v7-v1_00000_0532b03a-aec1-457f-a435-24e803c24678.root");
	fnames.push_back("relvalFiles/store_relval_CMSSW_11_3_0_pre5_RelValZTT_14_MINIAODSIM_113X_mcRun3_2021_realistic_v7-v1_00000_4de05cc1-37f0-4e4b-93d0-15c43b228124.root");
    doEfficiencyPlotsForASet(fnames,folder,suffix,tree_name,
                              bname_matchedGenP4,bname_matchedRecoP4,bname_missedGenP4,
                              pTmin);
    fnames.clear();




}

