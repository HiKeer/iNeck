using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class NewBehaviourScript : MonoBehaviour
{
    public GameObject StartView;
    public GameObject MusicView;
    public GameObject styleView;
    public GameObject player2;

    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {

    }

    public void StartButton()
    {
        StartView.SetActive(false);
        styleView.SetActive(true);
    }

    public void SetUpButton()
    {
        StartView.SetActive(false);
        MusicView.SetActive(true);
    }
    public void ReturnButton()
    {
        StartView.SetActive(true);
        styleView.SetActive(false);
        MusicView.SetActive(false);
    }

    public void ExitButton()
    {
#if UNITY_EDITOR
        UnityEditor.EditorApplication.isPlaying = false;
#else
        Application.Quit();
#endif
    }
    public void OnePlayer()
    {
        SceneManager.LoadScene("iNeck1Mod");        
    }
    public void TwoPlayer()
    {
        SceneManager.LoadScene("iNeck");
    }
}

