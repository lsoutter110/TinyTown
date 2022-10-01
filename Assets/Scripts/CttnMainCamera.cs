using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class CttnMainCamera : MonoBehaviour
{
    string status = "building";
    // Start is called before the first frame update
    void Start()
    {
        //ImgChange("SwitchPharse", "AttackingPharse");
    }

    // Update is called once per frame
    void Update()
    {
        MouseClick();
        switch (status){
            case "building":
                ImgChange("SwitchPharse", "BuildingPharse");
                BuildSomething();
                break;
            case "await-built":
                ImgChange("SwitchPharse", "BuildingPharse");
                break;
        }
    }

    public void MouseClick()
    {
        if (Input.GetMouseButtonUp(0)){
            Vector2 mousePosition = Camera.main.ScreenToWorldPoint(Input.mousePosition);
            GameObject.Find("ClickGridNum").GetComponent<Text>().text = getGrid(mousePosition);
            Debug.Log(getGrid(mousePosition));
        }        
    }

    public string getGrid(Vector2 coords)
    {
        //-4,73 to 4.73 width
        //-4.01 to 4.01 height
        double fullWidth = 4.73;
        double fullHeight = 4.01;
        double x = coords[0];
        double y = coords[1];

        x = x + fullWidth;
        double xlimiter = (fullWidth / 6);
        int xGrid = (int)Math.Floor(x / xlimiter) + 1;
    
        y = y + fullHeight;
        double ylimiter = (fullHeight / 6);
        int yGrid = (int)Math.Floor(y / ylimiter) + 1;

        string result = xGrid.ToString() + "," + yGrid.ToString();
        return (result);
    }

    public void ClickTownHall()
    {
        //GameObject.Find("ClickBuildingName").GetComponent<Text>().text = "Townhall";       
        string obname = GameObject.Find("ClickGridNum").GetComponent<Text>().text;
        if (obname != "") {
            ImgChange(obname, "Townhall");
        }
    }

    public void await_built(){
        //ImgChange("SwitchPharse", "AttackingPharse");
        status = "await-built";
    }

    public void BuildSomething(){
        // string obname = GameObject.Find("ClickGridNum").GetComponent<Text>().text;
        // if (obname) {
        //     ImgChange(obname, )
        // }
    }

    public void ImgChange(string ob, string imgName){
        Image imgPharse = GameObject.Find(ob).GetComponent<Image>(); 
        //Debug.Log(imgPharse);
        Sprite sp = Resources.Load("Pictures/" + imgName, typeof(Sprite)) as Sprite;
        //Sprite spb = Resources.Load("Pictures/Pharse", typeof(Sprite)) as Sprite;
        imgPharse.sprite = sp;  
    }
}
