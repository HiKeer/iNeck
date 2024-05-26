using System;
using System.Collections;
using System.Collections.Generic;
using System.Reflection.Emit;
using System.Threading;
using UnityEngine;


public class Player1 : MonoBehaviour
{
    PlayerInput1 playerInput1 ;
    [SerializeField] Transform[] LaneTransForm;
    [SerializeField] float JumpHeight = 1.0f;
    [SerializeField] Transform GrounCheckTransform;
    [SerializeField] [Range(0,1)] float GroundCheckRadius = 0.2f;
    [SerializeField] LayerMask GroundCheckMask;
    [SerializeField] public int CoinCount;
    Vector3 Destination;
    int CurrentLane;
    private double timeoffset;

    private void OnEnable() 
    {
        if(playerInput1==null){
            playerInput1 = new PlayerInput1();
        }
        playerInput1.Enable();
    }
    private void OnDisable() 
    {
        playerInput1.Disable();   
    }
    // Start is called before the first frame update
    void Start()
    {
        CoinCount = 0;
        for(int i=0;i<LaneTransForm.Length;i++){
            if(LaneTransForm[i].position == transform.position){
                CurrentLane = i;
                Destination = LaneTransForm[i].position;
            }
        };
        playerInput1.gameplay.Move.performed += MovePerformed;
        playerInput1.gameplay.Jump.performed += JumpPerformed;
        playerInput1.gameplay.Roll.performed += RollPerformed;
    }
    private void MoveLeft(){
        if(CurrentLane == 0){
            return;
        };
        CurrentLane--;
        Destination = LaneTransForm[CurrentLane].position;
    }
    private void MoveRight(){
        if(CurrentLane == LaneTransForm.Length -1){
            return;
        };
        CurrentLane++;
        Destination = LaneTransForm[CurrentLane].position;

    }
    private void MovePerformed(UnityEngine.InputSystem.InputAction.CallbackContext context)
    {
        float InputValue = context.ReadValue<float>();
        if(InputValue >0){
            MoveRight();
        }else if(InputValue < 0){
            MoveLeft();
        }
        //Debug.Log($"移动操作生效了，其值为{InputValue}");
    }
    private void JumpPerformed(UnityEngine.InputSystem.InputAction.CallbackContext context)
    {
        Rigidbody rigidbody = GetComponent<Rigidbody>();
        if(rigidbody!=null){
            float JumpSpeed = Mathf.Sqrt(2*JumpHeight*Physics.gravity.magnitude);
            rigidbody.AddForce(new Vector3(0,JumpSpeed,0),ForceMode.VelocityChange);
        };
    }
    private void RollPerformed(UnityEngine.InputSystem.InputAction.CallbackContext context)
    {
        Debug.Log("roll111111");
        this.gameObject.tag = "Rolling";
        timeoffset = DateTime.Now.TimeOfDay.TotalSeconds;
    }
    // Update is called once per frame
    void Update()
    {
        double gametime = DateTime.Now.TimeOfDay.TotalSeconds;
        if(gametime - timeoffset > 0.7){
            this.gameObject.tag = "NotRolling";
        }
        float TransformX = Mathf.Lerp(transform.position.x,Destination.x,Time.deltaTime*5);     
        transform.position = new Vector3(TransformX,transform.position.y,transform.position.z);   
        if(!IsOnGround()){
            //Debug.Log("不在地面上");
            OnDisable();
        }else{
            //Debug.Log("在地面上");
            OnEnable();
        }
    }
    void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Coin"){
            CoinCount++;
        }
    }

    bool IsOnGround(){
        return Physics.CheckSphere(GrounCheckTransform.position,GroundCheckRadius,GroundCheckMask);
    }
}
